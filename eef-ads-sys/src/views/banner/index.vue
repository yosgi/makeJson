<template>
  <div class="app-container">
    <div class="actionbar">
      <div class="right">
        <el-button type="danger" plain class="button" @click="add"
          >新增广告</el-button
        >
      </div>
    </div>
    <div class="actionbar">
      <div class="left">
        <span>搜索?</span>
        <el-input placeholder="标识" clearable v-model="param.slug" class="box">
        </el-input>
        <el-select
          placeholder="类型"
          v-model="param.video"
          clearable
          class="box"
        >
          <el-option
            v-for="item in type"
            :key="item.label"
            :label="item.label"
            :value="item.value"
          >
          </el-option>
        </el-select>
        <el-select
          placeholder="活动"
          v-model="param.campaign"
          clearable
          filterable
          class="box"
        >
          <el-option
            v-for="item in campaigns"
            :key="item"
            :label="item"
            :value="item"
          >
          </el-option>
        </el-select>
        <el-select
          placeholder="广告位"
          v-model="param.zones"
          clearable
          filterable
          class="box"
        >
          <el-option
            v-for="item in zones"
            :key="item"
            :label="item"
            :value="item"
          >
          </el-option>
        </el-select>
      </div>
      <div class="right">
        <el-button
          circle
          icon="el-icon-refresh-left"
          @click="reset"
        ></el-button>
        <el-button
          type="primary"
          circle
          plain
          icon="el-icon-search"
          @click="search"
        ></el-button>
      </div>
    </div>
    <el-table :data="banners" border stripe style="width: 100%">
      <el-table-column align="center" prop="slug" label="标识" />
      <el-table-column align="center" prop="image" label="图片">
        <template slot-scope="scope">
          <el-image
            class="img"
            :src="scope.row.image"
            fit="contain"
            :preview-src-list="[scope.row.image]"
            v-if="!scope.row.video"
          ></el-image>
          <span v-else>无</span>
        </template>
      </el-table-column>
      <el-table-column align="center" prop="video" label="视频">
        <template slot-scope="scope">
          <el-link
            v-if="scope.row.video"
            type="primary"
            @click="play(scope.row.video.sources[0].src)"
            >预览</el-link
          >
          <span v-else>无</span>
        </template>
      </el-table-column>
      <el-table-column align="center" prop="title" label="标题" />
      <el-table-column align="center" prop="url" label="链接" />
      <el-table-column align="center" prop="campaign" label="活动" />
      <el-table-column align="center" prop="zones" label="广告位">
        <template slot-scope="scope">
          <span v-html="'[' + scope.row.zones.join(']<br>[') + ']'"></span>
        </template>
      </el-table-column>
      <el-table-column align="center" prop="weight" label="权重" />
      <el-table-column align="center" fixed="right" label="操作" width="100">
        <template slot-scope="scope">
          <el-button type="text" @click="handler(scope.row)">编辑</el-button>
        </template>
      </el-table-column>
    </el-table>
    <div class="pager" v-if="all.length > size">
      <el-pagination
        :page-size="size"
        background
        layout="prev, pager, next, jumper"
        :total="all.length"
        :current-page="current"
        @current-change="handleCurrentChange"
      >
      </el-pagination>
    </div>
    <el-dialog
      :visible.sync="dialogVisible"
      width="720px"
      :destroy-on-close="true"
      custom-class="video-dialog"
    >
      <video controls preload class="video" ref="video" :src="src"></video>
    </el-dialog>
  </div>
</template>

<script>
import { size, pager, filter, getSlugs } from "@/utils/tool";
import { get } from "js-cookie";
export default {
  data() {
    return {
      dialogVisible: false,
      src: "",
      banners: [],
      all: [],
      pagerVisible: false,
      size: size,
      current: 1,
      param: {
        slug: "",
        video: "",
        campaign: "",
        zones: "",
      },
      type: [
        { label: "图片", value: false },
        { label: "视频", value: true },
      ],
      campaigns: [],
      zones: [],
    };
  },
  methods: {
    pager(p) {
      this.current = p;
      this.banners = pager(this.all, p);
    },
    handler(row) {
      for (let i = 0; i < this.$store.getters.data.banners.length; i++) {
        if (row == this.$store.getters.data.banners[i]) {
          this.$router.push({ path: `/banner/edit/${i}` });
          break;
        }
      }
    },
    add() {
      this.$router.push({ path: "/banner/add" });
    },
    handleCurrentChange(v) {
      this.pager(v);
    },
    search() {
      if (!this.param.slug && !this.param.campaign && !this.param.zones) {
        this.reset();
      }
      this.all = filter(this.$store.getters.data.banners, this.param);
      this.pager(1);
    },
    reset() {
      this.param.slug = "";
      this.all = this.$store.getters.data.banners;
      this.pager(1);
    },
    play(url) {
      this.dialogVisible = true;
      this.src = url;
      this.$nextTick(() => {
        this.$refs.video.play();
      });
    },
  },
  created() {
    this.reset();
    this.campaigns = getSlugs(this.$store, "campaigns");
    this.zones = getSlugs(this.$store, "zones");
  },
};
</script>

<style lang="scss" scoped>
.actionbar {
  overflow: hidden;
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 1px solid #f1f1f1;
  .left {
    float: left;
    white-space: nowrap;
    span {
      margin-right: 10px;
      color: #97a8be;
    }
    .box {
      width: 120px;
      margin-right: 20px;
    }
  }
  .right {
    float: right;
    min-width: 100px;
    text-align: center;
  }
  .button {
    width: 100px;
  }
}
.pager {
  padding: 40px 0;
  text-align: center;
}
.img {
  width: 60px;
  height: 60px;
}
.video {
  display: block;
  width: 720px;
}
</style>
