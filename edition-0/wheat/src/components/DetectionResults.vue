<template>
  <div class="detection-results">
    <h2>检测结果</h2>
    <el-table :data="results" style="width: 100%">
      <el-table-column prop="image" label="图像" width="150">
        <template #default="scope">
          <img :src="scope.row.image" alt="Detection" class="result-image" />
        </template>
      </el-table-column>
      <el-table-column prop="wheat_count" label="小麦数量">
        <template #default="scope">
          <div>{{ scope.row.wheat_count || 'N/A' }}</div>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="300">
        <template #default="scope">
          <el-button @click="openDialog(scope.row.image)" type="primary" size="small" class="action-btn">查看图片</el-button>
          <el-button @click="handleDownloadData(scope.row.image)" type="success" size="small" class="action-btn">下载数据</el-button>
          <el-button @click="handleDownloadImage(scope.row.image)" type="success" size="small" class="action-btn">下载图像</el-button>
        </template>
      </el-table-column>
    </el-table>
    <!-- 弹出对话框 -->
      <el-dialog
      v-model="dialogVisible"
      title="查看图片"
      width="50%"
      :before-close="handleClose"
    >
      <img :src="dialogImage" class="dialog-image" />
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleDownloadImage(dialogImage)">下载图片</el-button>
        </div>
      </template>
    </el-dialog>
    
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import { ElMessageBox } from 'element-plus'

const props = defineProps<{
  results: Array<{ image: string; wheat_count: number }>
}>()

const dialogVisible = ref(false)
const dialogImage = ref('')

// 打开查看图片对话框
const openDialog = (image: string) => {
  if (image) {
    console.log("1")
    dialogImage.value = image
    dialogVisible.value = true
  }
}

// 处理对话框关闭
const handleClose = (done: () => void) => {
  done()
}

// 处理下载数据（空实现）
const handleDownloadData = (image: string) => {
  // 实现下载数据的逻辑
  console.log(`下载数据: ${image}`)
}

// 处理下载图片
const handleDownloadImage = (image: string) => {
  if (image) {
    // 使用 window.open 打开图像在新窗口
    window.open(image, '_blank');
  }
}
</script>

<style scoped>
.detection-results {
  padding: 20px;
  border: 1px solid #dcdfe6;
  border-radius: 5px;
  background-color: #ffffff;
  margin-top: 20px;
}

.result-image {
  width: 100px;
  height: auto;
  object-fit: cover;
  cursor: pointer;
}

.action-btn {
  margin-right: 10px;
}

.dialog-image {
  width: 100%;
  height: auto;
  object-fit: contain;
}
/* debug */
el-dialog {
  border: 1px solid red;
}
</style>
