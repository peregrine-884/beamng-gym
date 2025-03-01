from setuptools import setup, find_packages

# 依存ライブラリをrequirements.txtから取得
def get_requirements_from_file():
    with open("requirements.txt") as f_in:
        return f_in.read().splitlines()

setup(
    # パッケージ名、pip installするときの名前
    name="beamng_gym",
    
    # バージョン
    version="0.1.0",
    
    # パッケージの説明
    description="Custom Gymnasium environment for BeamNG simulation",
    
    # __init__.pyを含むディレクトリを指定
    packages=find_packages(),
    
    # 依存ライブラリのインストール
    install_requires=get_requirements_from_file(),
    
    # JSON5設定ファイルを含める
    include_package_data=True,
    package_data={
        "beamng_gym": ["config/*.json5"]  # 設定ファイルを含める
    },
    
    # メタデータ
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    python_requires=">=3.7"
)
