def notifier = ""
def color_name="good"

pipeline {
  agent  {
    docker {
      image 'centos-node:latest'
      args "-v /data:/data -v /etc/passwd:/etc/passwd -v /etc/group:/etc/group -v /var/lib/jenkins:/var/lib/jenkins"
      reuseNode true
    }
  }
  environment {
    BASE_PATH="/opt/vhosts/wx-spider/"
    DATA_PATH="/data/vhosts/wx-spider/"
    RSYNC_PATH="${BASE_PATH}gitpull/"
    DEPLOY_PATH="${BASE_PATH}src/"
    KEEP_PKGS=5
    PKG_PATH="../"
    
    PKG_FORMAT="wxspider-%s.tar.gz"
    PKG_EXCLUDE_STR="  --exclude=\"*.map\" --exclude=.editorconfig  --exclude=.idea --exclude=*.md --exclude=.php_cs --exclude=.travis.yml --exclude=\"*@tmp\" --exclude=.git* "
    EXCLUDE_EXP="\\\\-\\\\-\\\\-|\\\\.git"

  }
  parameters {
    choice(name: 'ACTION_TYPE', choices: ['发布', '回滚'], description: '请选择发布 、回滚')
    string(name: "GITHUB_PROJECT", defaultValue: 'https://github.com/eefocus/tools.git', description: 'Github code repository')
    gitParameter description: 'Choose branch/tag', branchFilter: '.*', defaultValue: 'master', name: 'BRANCH_TAG', type: 'PT_BRANCH_TAG', quickFilterEnabled: true, tagFilter: '*', listSize: "12"
    string defaultValue: '192.168.88.92', description: 'Server_ips list', name: 'SERVER_IPS', trim: true
  }
  options {
    timeout(time: 45, unit: 'MINUTES')
    timestamps()
  }
  stages {
      
        stage("dispatch") {
          steps{
            script {
              ACTION_CHOSEN = "x"
              switch(ACTION_TYPE) {
                case "回滚":
                  ACTION_CHOSEN="回滚"
                  break
                default:
                  ACTION_CHOSEN="发布"
                  break;
              }
              configFileProvider([configFile(fileId: '47299b19-0338-473d-a65a-8da13057663a', targetLocation: '.git/NotiFile')]) {
                notifier = load ".git/NotiFile"
              }
              notifier.sendSlackMsg("${ACTION_CHOSEN} *Started*", "#3838d8")
            }
              
          }
        }
        
        stage("rollback") {
            when {
                expression { ACTION_CHOSEN == "回滚" }
            }
            steps {
                script {
                    IPS = SERVER_IPS.tokenize(",")
                    IP=IPS[0]
                    REMOTE_FILES=[:]

                    withCredentials([sshUserPrivateKey(credentialsId: 'rootk', keyFileVariable: 'ROOT_SSH_KEY_FILE', usernameVariable: 'ROOT_SSH_USER') ]) {
                        REMOTE_FILES = sh(returnStdout: true, script: "ssh -i ${ROOT_SSH_KEY_FILE} -o StrictHostKeyChecking=no ${ROOT_SSH_USER}@${IP} 'ls -t ${RSYNC_PATH}`printf ${PKG_FORMAT} \"*\"`' ").trim()

                    }
                    REMOTE_FILES_LIST = REMOTE_FILES.tokenize()
                    def PACKAGE_TAR = input message: '请选择', ok: '回滚',
                            parameters: [
                            choice(name: 'AVAILABLE_PACKAGES', choices: REMOTE_FILES_LIST, description: '可用项回滚项')]

                    DIFF_FILE = sh(returnStdout: true, script: "printf \"%s\" ${RSYNC_PATH}diff.rollback.`date +'%Y%m%d_%H%M%S'`.txt").trim()

                    for(IP in IPS) {
                      echo "Start to rollback to host: ${IP}.... >>>>>>>>>>>>"
                      withCredentials([sshUserPrivateKey(credentialsId: 'rootk', keyFileVariable: 'ROOT_SSH_KEY_FILE', usernameVariable: 'ROOT_SSH_USER'), sshUserPrivateKey(credentialsId: 'www', keyFileVariable: 'WWW_SSH_KEY_FILE', usernameVariable: 'WWW_SSH_USER')]) {
                          sh """
                                ssh -i ${WWW_SSH_KEY_FILE} -o StrictHostKeyChecking=no ${WWW_SSH_USER}@${IP} "
                                    cd ${DEPLOY_PATH};
                                    time diff -u0 <(find . -type f ! -type l | sort) <(tar -ztf $PACKAGE_TAR | sort ) | grep -vE \\"($EXCLUDE_EXP)\\" | grep -E '^\\\\-' | sed -e 's/^\\\\-//g' | xargs rm -frv >> $DIFF_FILE 2>&1
                                "
                          """
                        sh "ssh -i ${WWW_SSH_KEY_FILE} -o StrictHostKeyChecking=no ${WWW_SSH_USER}@${IP} 'tar -zpxf ${PACKAGE_TAR} -C ${DEPLOY_PATH}'"
                        
                        // delete packages that are more than $KEEP_PKGS
                        def SHELL_CMD="""
                        TOTAL_FILES=\\\$(ls ${RSYNC_PATH}`printf ${PKG_FORMAT} "*"` | wc -l)
                        for i in \\\$(ls -tr ${RSYNC_PATH}`printf ${PKG_FORMAT} "*"` | head -n \\\$(expr \\\$TOTAL_FILES - $KEEP_PKGS) ) ; do 
                            rm -fv \\\$i;
                        done;
                        """

                        sh """
                            ssh -i ${ROOT_SSH_KEY_FILE} -o StrictHostKeyChecking=no ${ROOT_SSH_USER}@${IP} "$SHELL_CMD"
                        """
                      }
                      echo "Rollback finished: ${IP} <<<<<<<<<<<<<."
                    }
                    
                }
            }
        }

    stage("pull") {
      when {
          expression { ACTION_CHOSEN == "发布" }
      }
      steps {
        script {
            sh "git config http.proxy http://103.91.219.139:15886 || true && git config https.proxy http://103.91.219.139:15886 || true"
            sh "git config --global http.proxy http://103.91.219.139:15886 || true && git config --global https.proxy http://103.91.219.139:15886 || true"

          checkout([$class: 'GitSCM', branches: [[name: "${params.BRANCH_TAG}"]], userRemoteConfigs: [[credentialsId: '2a657cb0-dbbe-4cf0-98b1-fe6e528c69c2', url: "${params.GITHUB_PROJECT}"]]])
          dir("wx-spider") {
            LINK_FILES=[
              "config.js": "${DATA_PATH}config.js"
            ]
            LINK_FILES.each { target, src ->
              sh "rm -fr ${target} || pwd"
              sh "ln -sf ${src} ${target}"
            }
          }
        }
      }
    }

    stage('build') {
      when {
          expression { ACTION_CHOSEN == "发布" }
      }
      steps {
        dir("wx-spider") {
          script {
            sh "npm config set proxy http://103.91.219.139:15886 && npm config set https-proxy http://103.91.219.139:15886"
            sh "rm -f package-lock.json"
            sh "npm install"
          }
        }
      }
    }

    stage('deploy') {
      when {
          expression { ACTION_CHOSEN == "发布" }
      }
      steps {
        dir("wx-spider") {
          script {
              PACKAGE_TAR = sh(returnStdout: true, script: """
                printf "${PKG_FORMAT}" `git describe`_`date +'%Y%m%d_%H%M%S'`
              """).trim()
              WORKSPACE_PKG_PATH="${PKG_PATH}${PACKAGE_TAR}"
              RSYNC_PKG_PATH="${RSYNC_PATH}${PACKAGE_TAR}"
              DIFF_FILE = sh(returnStdout: true, script: "printf \"%s\" ${RSYNC_PATH}diff.`date +'%Y%m%d_%H%M%S'`.txt").trim()
              sh "tar ${PKG_EXCLUDE_STR} -pzcf ${WORKSPACE_PKG_PATH} ."

              IPS = SERVER_IPS.split(",")
            for(IP in IPS) {
              echo "Start to deploy to host: ${IP}.... >>>>>>>>>>>>"
              withCredentials([sshUserPrivateKey(credentialsId: 'rootk', keyFileVariable: 'ROOT_SSH_KEY_FILE', usernameVariable: 'ROOT_SSH_USER'), sshUserPrivateKey(credentialsId: 'www', keyFileVariable: 'WWW_SSH_KEY_FILE', usernameVariable: 'WWW_SSH_USER')]) {
                  sh "ssh -i ${WWW_SSH_KEY_FILE} -o StrictHostKeyChecking=no ${WWW_SSH_USER}@${IP} 'mkdir -p ${DEPLOY_PATH} || true && mkdir -p ${RSYNC_PATH} || true'"

                  sh "rsync -e 'ssh -o StrictHostKeyChecking=no -i ${WWW_SSH_KEY_FILE}' -azp --partial ${WORKSPACE_PKG_PATH} ${WWW_SSH_USER}@${IP}:${RSYNC_PATH} "
                  sh """
                      ssh -i ${WWW_SSH_KEY_FILE} -o StrictHostKeyChecking=no ${WWW_SSH_USER}@${IP} "
                          cd ${DEPLOY_PATH};
                          time diff -u0 <(find . -type f ! -type l | sort) <(tar -ztf $RSYNC_PKG_PATH | sort ) | grep -vE \\"($EXCLUDE_EXP)\\" | grep -E '^\\\\-' | sed -e 's/^\\\\-//g' | xargs rm -frv >> $DIFF_FILE 2>&1
                      "
                  """
                  sh "ssh -i ${WWW_SSH_KEY_FILE} -o StrictHostKeyChecking=no ${WWW_SSH_USER}@${IP} 'tar -pzxf ${RSYNC_PKG_PATH} -C ${DEPLOY_PATH}'"

                  // delete packages that are more than $KEEP_PKGS
                  def SHELL_CMD="""
                  TOTAL_FILES=\\\$(ls ${RSYNC_PATH}`printf ${PKG_FORMAT} \"*\"` | wc -l)
                  for i in \\\$(ls -tr ${RSYNC_PATH}`printf ${PKG_FORMAT} \"*\"` | head -n \\\$(expr \\\$TOTAL_FILES - $KEEP_PKGS) ) ; do 
                      rm -fv \\\$i;
                  done;
                  """
                  sh """
                      ssh -i ${ROOT_SSH_KEY_FILE} -o StrictHostKeyChecking=no ${ROOT_SSH_USER}@${IP} "$SHELL_CMD"
                  """
              }
              echo "Deployed: ${IP} <<<<<<<<<<<<<."
            }
            
          }
        }
      }
    }
  }

  post {
    always {
      script {
        if(ACTION_CHOSEN == "发布") {
            dir("wx-spider") {
              sh "rm -fv ${PKG_PATH}`printf ${PKG_FORMAT} \"*\"`"
              sh "git config --unset http.proxy || true && git config --unset https.proxy || true"
              sh "git config --global --unset http.proxy || true && git config --global --unset https.proxy || true"
            }
            sh "git checkout . && git clean -f"
        }
        
        switch(currentBuild.currentResult) {
          case "SUCCESS":
            color_name="good"
            break;
          case "FAILURE":
            color_name="danger"
            break;
          // case "CHANGED":
          // case "UNSUCCESSFUL":
          // case "UNSTABLE":
          // case "ABORTED":
          default:
            color_name="#5f5f5f"
            break;
        }
        
        notifier.sendResultEmailNotification("${color_name}")
        
        
      }

    }
  }
}
