<template>
  <div class="app-container">
    <el-form
      ref="bannerAdd"
      :model="banner"
      :rules="rules"
      label-width="100px"
      class="form"
    >
      <el-form-item label="">
        <el-radio-group v-model="type">
          <el-radio-button label="图片"></el-radio-button>
          <el-radio-button label="视频"></el-radio-button>
        </el-radio-group>
      </el-form-item>
      <el-form-item label="图片/视频" prop="thing">
        <el-input v-model="banner.thing"></el-input>
      </el-form-item>
      <el-form-item label="标识" prop="slug">
        <el-input v-model="banner.slug"></el-input>
      </el-form-item>
      <el-form-item label="标题" prop="title">
        <el-input v-model="banner.title"></el-input>
      </el-form-item>
      <el-form-item label="链接" prop="url">
        <el-input v-model="banner.url"></el-input>
      </el-form-item>
      <el-form-item label="权重" prop="weight">
        <el-input v-model="banner.weight"></el-input>
      </el-form-item>
      <el-form-item label="活动" prop="campaign">
        <el-select placeholder="活动" v-model="banner.campaign" filterable>
          <el-option
            v-for="item in campaigns"
            :key="item"
            :label="item"
            :value="item"
          >
          </el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="广告位" prop="zones">
        <el-select
          placeholder="广告位"
          v-model="banner.zones"
          filterable
          multiple
        >
          <el-option
            v-for="item in zones"
            :key="item"
            :label="item"
            :value="item"
          >
          </el-option>
        </el-select>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" plain class="submit" @click="handler"
          >提交</el-button
        >
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
import { Message } from "element-ui";
import { exist, getSlugs } from "@/utils/tool";
export default {
  data() {
    return {
      id: 0,
      type: "图片",
      campaigns: [],
      zones: [],
      banner: {
        weight: 1,
        zones: [],
      },
      rules: {
        thing: [
          {
            required: true,
            message: "请填写图片或视频地址",
            trigger: "blur",
          },
        ],
        slug: [
          {
            required: true,
            message: "请填写唯一标识",
            trigger: "blur",
          },
        ],
        title: [
          {
            required: true,
            message: "请填写标题",
            trigger: "blur",
          },
        ],
        weight: [
          {
            required: true,
            message: "请填写权重",
            trigger: "blur",
          },
        ],
        campaign: [
          {
            required: true,
            message: "请选择活动",
            trigger: "change",
          },
        ],
        zones: [
          {
            required: true,
            message: "请选择广告位",
            trigger: "change",
          },
        ],
        url: [
          {
            required: true,
            message: "请填写跳转链接",
            trigger: "blur",
          },
        ],
      },
    };
  },
  methods: {
    handler() {
      this.$refs["bannerAdd"].validate((valid) => {
        if (valid) {
          if (this.type == "图片") {
            this.$store.dispatch("data/updateBanner", {
              id: this.id,
              data: {
                image: this.banner.thing,
                url: this.banner.url,
                title: this.banner.title,
                slug: this.banner.slug,
                weight: this.banner.weight,
                campaign: this.banner.campaign,
                zones: this.banner.zones,
              },
            });
          }
          if (this.type == "视频") {
            this.$store.dispatch("data/updateBanner", {
              id: this.id,
              data: {
                image: this.banner.thing,
                url: this.banner.url,
                title: this.banner.title,
                slug: this.banner.slug,
                weight: this.banner.weight,
                campaign: this.banner.campaign,
                zones: this.banner.zones,
                video: {
                  muted: true,
                  loop: true,
                  autoplay: true,
                  controlslist: "nodownload nofullscreen noremoteplayback",
                  disablepictureinpicture: true,
                  sources: [
                    {
                      src: this.banner.thing,
                      type: "video/mp4",
                    },
                  ],
                },
              },
            });
          }
          Message.success("提交成功！");
          this.$router.push({ path: "/banner/index" });
        } else {
          return false;
        }
      });
    },
  },
  created() {
    this.id = this.$route.params.id;
    let banner = JSON.parse(
      JSON.stringify(this.$store.getters.data.banners[this.id])
    );
    this.banner = {
      thing: banner.video ? banner.video.sources[0].src : banner.image,
      url: banner.url,
      title: banner.title,
      slug: banner.slug,
      weight: banner.weight,
      campaign: banner.campaign,
      zones: banner.zones,
    };
    this.type = banner.video ? "视频" : "图片";
    this.campaigns = getSlugs(this.$store, "campaigns");
    this.zones = getSlugs(this.$store, "zones");
  },
};
</script>

<style scoped>
.form {
  width: 50%;
}
.submit {
  width: 100px;
}
</style>
