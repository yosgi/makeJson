<template>
  <div class="app-container">
    <el-form
      ref="campaignEdit"
      :model="campaign"
      :rules="rules"
      label-width="100px"
      class="form"
    >
      <el-form-item label="标识" prop="slug">
        <el-input disabled v-model="campaign.slug"></el-input>
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
export default {
  data() {
    return {
      id: 0,
      campaign: {},
      rules: {
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
      this.$refs["campaignEdit"].validate((valid) => {
        if (valid) {
          this.$store.dispatch("data/updateCampaign", {
            id: this.id,
            data: this.campaign,
          });
          Message.success("提交成功！");
          this.$router.push({ path: "/campaign/index" });
        } else {
          return false;
        }
      });
    },
  },
  created() {
    this.id = this.$route.params.id;
    this.campaign = JSON.parse(JSON.stringify(this.$store.getters.data.campaigns[this.id]));
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
