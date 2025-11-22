import os
import shutil
import zipfile
from datetime import datetime
import subprocess


def create_release_package():
    """简化的发布包制作函数"""
    print("🎓 审计2501班高数成绩查询系统 - 打包工具")
    print("=" * 50)

    # 检查必要文件
    required_files = ['app.py', 'index.html', 'ccScoreSearch.py']
    for file in required_files:
        if not os.path.exists(file):
            print(f"❌ 缺少文件: {file}")
            return

    print("✅ 必要文件检查通过")

    # 清理之前的构建
    for folder in ['build', 'dist']:
        if os.path.exists(folder):
            shutil.rmtree(folder)
            print(f"🧹 已清理: {folder}")

    # 安装依赖
    print("📦 安装依赖...")
    try:
        subprocess.check_call(['pip', 'install', 'flask==2.3.3', 'flask-cors==4.0.0', 'pyinstaller'])
        print("✅ 依赖安装完成")
    except Exception as e:
        print(f"❌ 依赖安装失败: {e}")
        return

    # 打包exe
    print("🔨 打包应用程序...")
    try:
        subprocess.check_call([
            'pyinstaller', '--onefile', '--add-data', 'index.html;.',
            '--name', 'ccScoreSearch', '--console', '--clean', 'app.py'
        ])
        print("✅ 应用程序打包完成")
    except Exception as e:
        print(f"❌ 打包失败: {e}")
        return

    # 创建发布目录
    release_dir = "ccScoreSearch_发布包"
    if os.path.exists(release_dir):
        shutil.rmtree(release_dir)
    os.makedirs(release_dir)

    # 复制文件
    shutil.copy('dist/ccScoreSearch.exe', release_dir)

    # 创建使用说明
    with open(f'{release_dir}/使用说明.txt', 'w', encoding='utf-8') as f:
        f.write(f"""审计2501班高数成绩查询系统
版本: 1.0
打包时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

使用说明:
1. 双击运行"启动系统.bat"
2. 在浏览器访问 http://localhost:5000
3. 输入学号或姓名查询成绩

注意事项:
• 确保5000端口未被占用
• 首次运行请允许防火墙访问
""")

    # 创建启动脚本 (保持不变)
    with open(f'{release_dir}/启动系统.bat', 'w', encoding='utf-8') as f:
        f.write("""@echo off
chcp 65001 >nul
title 审计2501班高数成绩查询系统

echo.
echo ═══════════════════════════════════════════
echo   审计2501班高数成绩查询系统 v1.0
echo ═══════════════════════════════════════════
echo.
echo 📊 系统启动中...
echo 🌐 启动完成后请在浏览器中访问: http://localhost:5000
echo.
echo ⚠️  注意事项:
echo    • 请确保5000端口未被占用
echo    • 首次运行防火墙可能提示，请选择允许
echo    • 按 Ctrl+C 可停止系统
echo.

timeout /t 3 /nobreak >nul

echo 🚀 启动服务器...
echo.
ccScoreSearch.exe

if errorlevel 1 (
    echo.
    echo ❌ 系统启动失败！
    echo 💡 可能的原因:
    echo    • 5000端口被占用
    echo    • 缺少运行库
    echo    • 防火墙阻止
    echo.
    echo 🔧 请尝试:
    echo    • 以管理员身份运行
    echo    • 检查端口占用
    echo    • 查看使用说明.txt
)

echo.
pause
""")

    # 创建ZIP包
    zip_filename = f"ccScoreSearch_发布包_{datetime.now().strftime('%Y%m%d_%H%M')}.zip"

    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file in os.listdir(release_dir):
            file_path = os.path.join(release_dir, file)
            zipf.write(file_path, file)

    # 显示结果
    exe_size = os.path.getsize('dist/ccScoreSearch.exe') / (1024 * 1024)
    zip_size = os.path.getsize(zip_filename) / (1024 * 1024)

    print(f"\n📊 打包完成!")
    print(f"   • 主程序: {exe_size:.1f} MB")
    print(f"   • 发布包: {zip_size:.1f} MB")
    print(f"   • 文件位置: {zip_filename}")

    # 清理临时文件
    cleanup = input("\n是否清理临时文件? (y/n): ").lower()
    if cleanup in ['y', 'yes', '是']:
        for folder in ['build', 'dist']:
            if os.path.exists(folder):
                shutil.rmtree(folder)
        print("✅ 临时文件已清理")

    print(f"\n🎉 完成! 请发送 {zip_filename} 给用户")


if __name__ == '__main__':
    create_release_package()