<template>
  <div>
    <el-row :gutter="20" justify="center" align="middle" class="container">
      <el-col :span="10">
        <el-card class="custom-card hover">
          <template #header>
            <div class="card-header">
              <span>图片上传</span>
            </div>
          </template>
          <el-upload
            v-model:file-list="imageFileList"
            class="upload-demo"
            action="/upload/image"
            :http-request="uploadImageFile"
            :on-preview="handleImagePreview"
            :on-remove="handleImageRemove"
            list-type="picture"
          >
            <el-button type="primary">点击上传图片</el-button>
            <template #tip>
              <div class="el-upload__tip">
                上传大小不超过500kb的jpg/png文件
              </div>
            </template>
          </el-upload>
        </el-card>
      </el-col>
      <el-col :span="10">
        <el-card class="custom-card hover">
          <template #header>
            <div class="card-header">
              <span>视频上传</span>
            </div>
          </template>
          <el-upload
            v-model:file-list="videoFileList"
            class="upload-demo"
            action="/upload/video"
            :http-request="uploadVideoFile"
            :on-preview="handleVideoPreview"
            :on-remove="handleVideoRemove"
            list-type="picture"
          >
            <el-button type="primary">点击上传视频</el-button>
            <template #tip>
              <div class="el-upload__tip">
                上传大小不超过500mb的mp4文件
              </div>
            </template>
          </el-upload>
        </el-card>
      </el-col>
    </el-row>
    <detection-results :results="results" v-if="results.length > 0" />
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue';
import axios from 'axios';
import DetectionResults from './DetectionResults.vue';

import type { UploadProps, UploadUserFile } from 'element-plus';

const fileList = ref<UploadUserFile[]>([]);
const imageFileList = ref<UploadUserFile[]>([]);
const videoFileList = ref<UploadUserFile[]>([]);
const results = ref<Array<{ image: string; wheat_count: number }>>([]);

const handleImagePreview: UploadProps['onPreview'] = (file) => {
  console.log('图片预览:', file);
};

const handleImageRemove: UploadProps['onRemove'] = (file, fileList) => {
  console.log('移除图片:', file, fileList);
};

const handleVideoPreview: UploadProps['onPreview'] = (file) => {
  console.log('视频预览:', file);
};

const handleVideoRemove: UploadProps['onRemove'] = (file, fileList) => {
  console.log('移除视频:', file, fileList);
};



const uploadImageFile = async (options: any) => {
  const { file } = options;
  const formData = new FormData();
  formData.append('file', file);

  try {
    const response = await axios.post('http://127.0.0.1:5000/upload/image', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });

    results.value.push({
      image: `http://127.0.0.1:5000/results/${file.name}`,
      wheat_count: response.data.wheat_count,
    });
  } catch (error) {
    console.error('Error uploading image file:', error);
  }
};

const uploadVideoFile = async (options: any) => {
  const { file } = options;
  const formData = new FormData();
  formData.append('file', file);

  try {
    const response = await axios.post('http://127.0.0.1:5000/upload/video', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });

    // 如果需要处理视频结果，可以在这里处理
    console.log('视频上传成功', response.data);
  } catch (error) {
    console.error('Error uploading video file:', error);
  }
};
</script>

<style scoped>
.custom-card {
  margin-top: 20px;
  max-width: 480px;
  margin-bottom: 20px;
  transition: transform 0.3s ease;
  background-color: #ffffff;
}

.custom-card:hover {
  transform: scale(1.05);
  background-color: #98ea98;
}


</style>