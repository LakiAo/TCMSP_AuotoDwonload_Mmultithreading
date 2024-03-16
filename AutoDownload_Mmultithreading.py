import requests
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

# 设置保存下载文件的目录
save_dir = 'Downloaded'
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

def download_file(url_save_tuple):
    """下载文件并保存到指定路径"""
    url, save_path = url_save_tuple
    try:
        r = requests.get(url, stream=True)
        if r.status_code == 200:
            with open(save_path, 'wb') as f:
                f.write(r.content)
            return f"文件已下载并保存到 {save_path}"
        else:
            return f"无法下载文件：{url}，状态码：{r.status_code}"
    except Exception as e:
        return f"下载文件时出现错误：{e}"

def main():
    base_url = "https://old.tcmsp-e.com/tcmspmol/MOL"
    urls_and_save_paths = []

    for i in range(1, 14250):  # 从1到14249，包含14249
        file_number = str(i).zfill(6)  # 将数字转换为字符串，前面填充0至6位
        file_url = f"{base_url}{file_number}.mol2"
        save_path = os.path.join(save_dir, f"MOL{file_number}.mol2")
        urls_and_save_paths.append((file_url, save_path))

    # 设置线程池的大小，16个线程
    with ThreadPoolExecutor(max_workers=16) as executor:
        # 使用executor.map来并发执行下载和保存文件
        future_to_url = {executor.submit(download_file, url_save): url_save for url_save in urls_and_save_paths}
        for future in as_completed(future_to_url):
            url_save = future_to_url[future]
            try:
                data = future.result()
                print(data)
            except Exception as exc:
                print(f"{url_save[0]} 生成了一个异常: {exc}")

if __name__ == "__main__":
    main()
