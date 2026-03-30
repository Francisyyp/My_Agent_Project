from langchain_experimental.utilities import PythonREPL
from langchain_core.tools import tool
import matplotlib
# 【核心修改】强制使用 Agg 后端，防止 macOS GUI 冲突
matplotlib.use('Agg') 
import matplotlib.pyplot as plt

repl = PythonREPL()

@tool
def python_repl_tool(code: str):
    """
    一个 Python 交互式环境。可以用它来处理数据或绘制图表。
    注意：已经预设了 matplotlib.use('Agg')。
    绘制完毕后，请务必使用 plt.savefig('chart.png')。
    """
    try:
        # 为了保险，在执行代码前强制注入后端设置
        full_code = "import matplotlib\nmatplotlib.use('Agg')\nimport matplotlib.pyplot as plt\n" + code
        result = repl.run(full_code)
        return f"执行成功。输出结果: {result}"
    except Exception as e:
        return f"执行出错: {str(e)}"