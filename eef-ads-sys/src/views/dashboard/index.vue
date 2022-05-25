<template>
  <div class="dashboard-container">
    <div class="dashboard-text">简单广告系统 V3.0</div>
    <p class="warning">所有操作均缓存在本地，点击更新上传到线上，否则无法保存！</p>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  name: 'Dashboard',
  computed: {
    ...mapGetters([
      'name'
    ])
  }
}
</script>

<style lang="scss" scoped>
.dashboard {
  &-container {
    margin: 30px;
  }
  &-text {
    font-size: 30px;
    line-height: 46px;
  }
}
.warning {
  color: #F56C6C;
}
</style>
