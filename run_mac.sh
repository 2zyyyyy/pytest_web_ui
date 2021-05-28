# 使用pytest生成原始报告，里面大多数是一些原始的json数据
pytest --alluredir Output/report_json

# 使用generate命令导出HTML报告到新的目录（-c 在生成报告之前先清理之前的报告目录，-o 指定生成报告的文件夹）
allure generate Output/report_json -c -o Output/report_allure

# 使用open命令在浏览器中打开HTML报告
allure open Output/report_allure