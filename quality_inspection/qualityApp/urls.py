from django.urls import path

from qualityApp import uploadViews, scoreViews, planViews, loginViews, scoreSqlMethod, scoreLogicMethod

urlpatterns = [
    # 录音上传模块
    # audio页面
    path('audioController/taskList', uploadViews.task_list),
    path('audioController/createTask', uploadViews.create_task),
    path('audioController/deleteTaskName', uploadViews.delete_task_name),
    path('audioController/editTaskName', uploadViews.edit_task_name),
    path('audioController/uploadFile', uploadViews.upload_file),
    # detail页面
    path('detailController/recordList', uploadViews.record_list),
    path('detailController/batchDeleteAudio', uploadViews.batch_delete_audio),
    path('detailController/deleteAudio', uploadViews.delete_audio),
    path('detailController/uploadFile', uploadViews.upload_file),

    # 质检评分模块
    # score页面
    path('scoreController/directoryList', scoreViews.directory_list),
    path('scoreController/updateDirectoryName', scoreViews.update_directory_name),
    path('scoreController/deleteDirectoryName', scoreViews.delete_directory_name),
    path('scoreController/qualityInspection', scoreViews.quality_inspection),

    # file页面
    path('fileController/resultList', scoreViews.result_list),
    path('fileController/deleteResult', scoreViews.delete_result),
    # quality页面
    path('qualityController/lastResult', scoreViews.last_result),
    path('qualityController/nextResult', scoreViews.next_result),
    path('qualityController/detailResult', scoreViews.detail_result),
    path('qualityController/editResult', scoreViews.edit_result),
    path('qualityController/getLrcFile', scoreViews.get_lrc_file),
    path('qualityController/getRecordFile', scoreViews.get_record_file),
    path('qualityController/keywordTimeResult', scoreViews.keyword_time_result),
    # 方案维护模块
    # plan页面
    path('planController/planList', planViews.plan_list),
    path('planController/EditPlan', planViews.edit_plan),
    # design页面
    path('designController/planSelect', planViews.plan_select),
    path('designController/seriesList', planViews.series_list),
    path('designController/createSeries', planViews.create_series),
    path('designController/updateSeries', planViews.update_series),
    path('designController/deleteSeries', planViews.delete_series),
    path('designController/batchDeleteSeries', planViews.batch_delete_series),
    path('designController/uploadSeries', planViews.upload_series),
    # keyword页面
    path('compileController/createKeyword', planViews.create_keyword),
    path('compileController/keyWordList', planViews.key_word_list),
    path('compileController/lastSeries', planViews.last_series),
    path('compileController/nextSeries', planViews.next_series),
    path('compileController/editKeyword', planViews.edit_keyword),
    path('compileController/deleteKeyword', planViews.delete_keyword),
    path('compileController/batchDeleteKeyword', planViews.batch_delete_keyword),
    # 登陆模块
    path('loginController/myLogin', loginViews.my_login),
    path('loginController/register', loginViews.register),
    path('loginController/loginOut', loginViews.login_out),
]
