<template>
  <div class="app-container">
    <el-form
      ref="campaignAdd"
      :model="campaign"
      :rules="rules"
      label-width="100px"
      class="form"
    >
      <el-form-item label="标识" prop="slug">
        <el-input v-model="campaign.slug"></el-input>
      </el-form-item>
      <el-form-item label="开始时间" prop="activate_time">
        <el-date-picker
          v-model="campaign.activate_time"
          type="datetime"
          placeholder="选择日期时间"
          format="yyyy/MM/dd HH:mm:ss"
          value-format="yyyy/MM/dd HH:mm:ss"
        >
        </el-date-picker>
      </el-form-item>
      <el-form-item label="结束时间" prop="expire_time">
        <el-date-picker
          v-model="campaign.expire_time"
          type="datetime"
          placeholder="选择日期时间"
          format="yyyy/MM/dd HH:mm:ss"
          value-format="yyyy/MM/dd HH:mm:ss"
        >
        </el-date-picker>
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
import { exist } from "@/utils/tool";
export default {
  data() {
    return {
      campaign: {},
      rules: {
        slug: [
          {
            required: true,
            message: "请填写唯一标识",
            trigger: "blur",
          },
        ],
        activate_time: [
          {
            required: true,
            message: "请选择日期时间",
            trigger: "change",
          },
        ],
        expire_time: [
          {
            required: true,
            message: "请选择日期时间",
            trigger: "change",
          },
        ],
      },
    };
  },
  methods: {
    handler() {
      this.$refs["campaignAdd"].validate((valid) => {
        if (valid) {
          if(exist(this.$store.getters.data.campaigns, 'slug', this.campaign.slug)) {
            Message.error("已存在的活动！");
            return false;
          }
          this.$store.dispatch("data/addCampaign", this.campaign);
          Message.success("提交成功！");
          this.$router.push({ path: "/campaign/index" });
        } else {
          return false;
        }
      });
    },
  },
  created() {},
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
