import Vue from 'vue'
import Router from 'vue-router'
import Layout from '@/components/Layout'//页面框架
import ScoreDirectory from '@/views/qualityScore/ScoreDirectory'//评分目录页面
import ScoreFile from '@/views/qualityScore/ScoreFile'//评分文件页面
import QualityDetail from '@/views/qualityScore/QualityDetail'//质检评分详情页面
import UploadAudio from '@/views/uplaodRecord/UploadAudio'//录音上传页面
import AudioDetail from '@/views/uplaodRecord/AudioDetail'//音频详细页面
import Login from '@/components/login'//登录页面
import PlanQuality from '@/views/planMaintenance/PlanQuality'//方案维护首页
import PlanDesign from '@/Views/planMaintenance/PlanDesign' //方案修改页面
import PlanCompile from '@/Views/planMaintenance/PlanCompile' //方案编辑页面
import StatisticalScore from '@/views/StatisticalChart/StatisticalScore'//质检图表页面

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Login',
      component: Login
    },
    {
      path: '',
      component: Layout,
      children: [
        {
          path: '/scoredirectory',
          name: 'scoredirectory',
          component: ScoreDirectory
        },
        {
          path: '/scorefile',
          name: 'scorefile',
          component: ScoreFile,
          meta:{
            guidePath: true,
            jumpPath: '/scoredirectory'
          }
        },
        {
          path: '/qualitydetail',
          name: 'qualitydetail',
          component: QualityDetail,
          meta:{
            guidePath: true,
            jumpPath: '/scoredirectory'
          }
        },
        {
          path: '/uploadaudio',
          name: 'uploadaudio',
          component: UploadAudio
        },
        {
          path: '/planquality',
          name: 'planquality',
          component: PlanQuality
        },
        {
          path: '/plandesign',
          name: 'plandesign',
          component: PlanDesign,
          meta:{
            guidePath: true,
            jumpPath: '/planquality'
          }
        },
        {
          path: '/plancompile',
          name: 'plancompile',
          component: PlanCompile,
          meta:{
            guidePath: true,
            jumpPath: '/planquality'
          }
        },
        {
          path: '/audiodetail',
          name: 'audiodetail',
          component: AudioDetail,
          meta:{
            guidePath: true,
            jumpPath: '/uploadaudio'
          }
        },
        {
          path: '/statisticalscore',
          name: 'statisticalscore',
          component: StatisticalScore
        },
      ]
    },
  ]
})
