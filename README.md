HCShop 自动化测试项目
这是一个针对 HCShop 电商系统的自动化测试项目，包含 UI 和 API 两层测试，
使用 Pytest + Allure 生成可视化测试报告。
 技术栈
- Python 3.10+
- Pytest（测试框架）
- Selenium UI 测试）
- Requests（API 测试）
- Allure（测试报告）
hcshop/
├── api_pages/ # API 封装层
├── pages/ # UI 页面对象模型
├── test/
  ————ui
  ____api # 测试用例（api/ + ui/）
├── utils/ # 工具类（浏览器驱动、请求处理）
├── data/ 
├── screenshots/ # 失败截图
├── .github/workflows/
└── conftest.py # Pytest 配置
# 运行测试并生成原始数据
pytest --alluredir=allure-results

# 生成 HTML 报告
allure generate allure-results -o allure-report --clean

# 在本地打开报告
allure open allure-report
