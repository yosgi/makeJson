<template>
  <div id="app">
    <router-view />
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>
<style lang="scss">
.video-dialog {
  .el-dialog__header {
    padding: 0;
    position: relative;
    z-index: 10;
    .el-dialog__headerbtn {
      position: absolute;
      right: 0;
      top: 0;
      font-size: 40px;
    }
  }
  .el-dialog__body {
    padding: 0;
  }
}
</style>
