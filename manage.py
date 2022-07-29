from myapp import create_app

if __name__ == "__main__":
    confPath = r"C:\1_code\tools_dmsedt\myapp\conf\conf.ini"
    app = create_app(confPath)
    app.run(host="127.0.0.1", port=12356)
