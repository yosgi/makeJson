<template>
  <div class="app-container">
    <div class="actionbar">
      <div class="right">
        <el-button type="danger" plain class="button" @click="add"
          >新增广告位</el-button
        >
      </div>
    </div>
    <div class="actionbar">
      <div class="left">
        <span>搜索?</span>
        <el-input placeholder="标识" clearable v-model="param.slug" class="box">
        </el-input>
        <el-select
          clearable
          v-model="param.type"
          placeholder="类型"
          class="box"
        >
          <el-option
            v-for="item in type"
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
    <el-table :data="zones" border stripe style="width: 100%">
      <el-table-column align="center" prop="slug" label="标识" />
      <el-table-column align="center" prop="width" label="宽度" />
      <el-table-column align="center" prop="height" label="高度" />
      <el-table-column align="center" prop="type" label="类型" />
      <el-table-column align="center" label="Cookie">
        <template slot-scope="scope">
          <span>{{
            scope.row.type == "banner"
              ? "无"
              : scope.row.settings.cookie_pattern
          }}</span>
        </template>
      </el-table-column>
      <el-table-column align="center" label="冷却时长">
        <template slot-scope="scope">
          <span>{{
            scope.row.type == "banner"
              ? "无"
              : scope.row.settings.refractory_period
          }}</span>
        </template>
      </el-table-column>
      <el-table-column align="center" label="延迟打开">
        <template slot-scope="scope">
          <span>{{
            scope.row.type == "banner"
              ? "无"
              : scope.row.settings.open_after
          }}</span>
        </template>
      </el-table-column>
      <el-table-column align="center" label="定时关闭">
        <template slot-scope="scope">
          <span>{{
            scope.row.type == "banner"
              ? "无"
              : scope.row.settings.close_after
          }}</span>
        </template>
      </el-table-column>
      <el-table-column align="center" label="展示位置">
        <template slot-scope="scope">
          <span>{{
            scope.row.type == "banner"
              ? "无"
              : scope.row.settings.position
          }}</span>
        </template>
      </el-table-column>
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
  </div>
</template>

<script>
import { size, pager, filter } from "@/utils/tool";
export default {
  data() {
    return {
      zones: [],
      all: [],
      pagerVisible: false,
      size: size,
      current: 1,
      param: {
        slug: "",
        type: "",
      },
      type: ["banner", "billboard"],
    };
  },
  methods: {
    pager(p) {
      this.current = p;
      this.zones = pager(this.all, p);
    },
    handler(row) {
      for (let i = 0; i < this.$store.getters.data.zones.length; i++) {
        if (row.slug == this.$store.getters.data.zones[i].slug) {
          this.$router.push({ path: `/zone/edit/${i}` });
          break;
        }
      }
    },
    add() {
      this.$router.push({ path: "/zone/add" });
    },
    handleCurrentChange(v) {
      this.pager(v);
    },
    search() {
      if (!this.param.slug && !this.param.type) {
        this.reset();
      }
      this.all = filter(this.$store.getters.data.zones, this.param);
      this.pager(1);
    },
    reset() {
      this.param.slug = "";
      this.all = this.$store.getters.data.zones;
      this.pager(1);
    },
  },
  created() {
    this.reset();
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
</style>
