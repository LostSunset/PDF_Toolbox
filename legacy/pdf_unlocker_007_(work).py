import os
import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import sys
import shutil

def install_package(package):
    """安裝缺少的套件"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        return True
    except:
        return False

def check_and_install_packages():
    """檢查並安裝必要的套件"""
    packages = {
        'pikepdf': 'pikepdf',
        'PyPDF2': 'PyPDF2', 
        'fitz': 'PyMuPDF',
        'reportlab': 'reportlab'
    }
    
    available_packages = {}
    
    for module_name, package_name in packages.items():
        try:
            __import__(module_name)
            available_packages[module_name] = True
            print(f"✓ {package_name} 已安裝")
        except ImportError:
            print(f"✗ {package_name} 未安裝，正在嘗試安裝...")
            if install_package(package_name):
                try:
                    __import__(module_name)
                    available_packages[module_name] = True
                    print(f"✓ {package_name} 安裝成功")
                except:
                    available_packages[module_name] = False
                    print(f"✗ {package_name} 安裝失敗")
            else:
                available_packages[module_name] = False
                print(f"✗ {package_name} 安裝失敗")
    
    return available_packages

def repair_pdf_with_pikepdf(file_path, output_path, password=None):
    """使用pikepdf修復PDF"""
    try:
        import pikepdf
        with pikepdf.open(file_path, password=password or "", allow_overwriting_input=True) as pdf:
            pdf.save(output_path)
        return True, "pikepdf成功"
    except Exception as e:
        return False, f"pikepdf失敗: {str(e)}"

def repair_pdf_with_pypdf2(file_path, output_path, password=None):
    """使用PyPDF2修復PDF"""
    try:
        import PyPDF2
        from PyPDF2 import PdfReader, PdfWriter
        
        with open(file_path, 'rb') as file:
            reader = PdfReader(file)
            
            # 如果有密碼，嘗試解密
            if reader.is_encrypted and password:
                reader.decrypt(password)
            elif reader.is_encrypted and not password:
                # 嘗試空密碼
                reader.decrypt("")
            
            writer = PdfWriter()
            
            # 複製所有頁面
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                writer.add_page(page)
            
            # 保存
            with open(output_path, 'wb') as output_file:
                writer.write(output_file)
        
        return True, "PyPDF2成功"
    except Exception as e:
        return False, f"PyPDF2失敗: {str(e)}"

def repair_pdf_with_pymupdf(file_path, output_path, password=None):
    """使用PyMuPDF修復PDF"""
    try:
        import fitz  # PyMuPDF
        
        # 打開PDF
        doc = fitz.open(file_path)
        
        # 如果需要密碼
        if doc.needs_pass and password:
            doc.authenticate(password)
        elif doc.needs_pass and not password:
            doc.authenticate("")  # 嘗試空密碼
        
        # 創建新文檔
        new_doc = fitz.open()
        
        # 複製所有頁面
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            new_doc.insert_pdf(doc, from_page=page_num, to_page=page_num)
        
        # 保存
        new_doc.save(output_path)
        new_doc.close()
        doc.close()
        
        return True, "PyMuPDF成功"
    except Exception as e:
        return False, f"PyMuPDF失敗: {str(e)}"

def repair_pdf_with_gs(file_path, output_path):
    """使用Ghostscript修復PDF"""
    try:
        # 嘗試找到Ghostscript
        gs_commands = ['gs', 'gswin64c', 'gswin32c', 'ghostscript']
        gs_cmd = None
        
        for cmd in gs_commands:
            try:
                subprocess.run([cmd, '--version'], capture_output=True, check=True)
                gs_cmd = cmd
                break
            except:
                continue
        
        if not gs_cmd:
            return False, "Ghostscript未安裝"
        
        # Ghostscript命令
        cmd = [
            gs_cmd,
            '-sDEVICE=pdfwrite',
            '-dCompatibilityLevel=1.4',
            '-dPDFSETTINGS=/prepress',
            '-dNOPAUSE',
            '-dQUIET',
            '-dBATCH',
            f'-sOutputFile={output_path}',
            file_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0 and os.path.exists(output_path):
            return True, "Ghostscript成功"
        else:
            return False, f"Ghostscript失敗: {result.stderr}"
    
    except Exception as e:
        return False, f"Ghostscript錯誤: {str(e)}"

def simple_pdf_copy(file_path, output_path):
    """簡單複製PDF檔案"""
    try:
        shutil.copy2(file_path, output_path)
        return True, "簡單複製成功"
    except Exception as e:
        return False, f"複製失敗: {str(e)}"

def repair_and_unlock_pdf(file_path, output_path, password=None, available_packages=None):
    """使用多種方法修復並解鎖PDF"""
    if available_packages is None:
        available_packages = {}
    
    methods = []
    
    # 根據可用套件添加修復方法
    if available_packages.get('fitz', False):
        methods.append(("PyMuPDF", repair_pdf_with_pymupdf))
    
    if available_packages.get('PyPDF2', False):
        methods.append(("PyPDF2", repair_pdf_with_pypdf2))
    
    if available_packages.get('pikepdf', False):
        methods.append(("pikepdf", repair_pdf_with_pikepdf))
    
    # 添加Ghostscript方法
    methods.append(("Ghostscript", repair_pdf_with_gs))
    
    # 最後嘗試簡單複製
    methods.append(("簡單複製", simple_pdf_copy))
    
    # 逐一嘗試每種方法
    for method_name, method_func in methods:
        try:
            print(f"  嘗試 {method_name}...")
            
            if method_name == "Ghostscript":
                success, message = method_func(file_path, output_path)
            elif method_name == "簡單複製":
                success, message = method_func(file_path, output_path)
            else:
                success, message = method_func(file_path, output_path, password)
            
            if success:
                # 檢查輸出檔案是否真的存在且不為空
                if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
                    return True, f"{method_name}成功"
                else:
                    print(f"  {method_name} 產生的檔案無效")
                    continue
            else:
                print(f"  {method_name} 失敗: {message}")
        
        except Exception as e:
            print(f"  {method_name} 執行錯誤: {str(e)}")
            continue
    
    return False, "所有修復方法都失敗了"

def unlock_pdfs():
    print("正在檢查並安裝必要套件...")
    available_packages = check_and_install_packages()
    
    if not any(available_packages.values()):
        messagebox.showerror("錯誤", "無法安裝任何PDF處理套件，請手動安裝:\npip install PyMuPDF PyPDF2 pikepdf")
        return
    
    # 選擇一個或多個PDF檔案
    root = tk.Tk()
    root.withdraw()  # 隱藏主窗口
    file_paths = filedialog.askopenfilenames(
        title="選擇要解鎖的PDF檔案",
        filetypes=[("PDF檔案", "*.pdf")]
    )
    
    if not file_paths:
        messagebox.showinfo("提示", "未選擇任何檔案")
        return
    
    success_count = 0
    failed_files = []
    success_details = []
    
    print(f"\n開始處理 {len(file_paths)} 個檔案...")
    
    for i, file_path in enumerate(file_paths, 1):
        try:
            # 獲取檔案路徑和檔名
            file_dir = os.path.dirname(file_path)
            file_name = os.path.basename(file_path)
            file_name_without_ext = os.path.splitext(file_name)[0]
            
            print(f"\n[{i}/{len(file_paths)}] 正在處理: {file_name}")
            
            # 創建輸出檔案路徑
            if "_已解鎖" in file_name_without_ext:
                base_name = file_name_without_ext.replace("_已解鎖", "")
                output_path = os.path.join(file_dir, f"{base_name}_重新修復.pdf")
            else:
                output_path = os.path.join(file_dir, f"{file_name_without_ext}_已修復.pdf")
            
            # 避免檔案名衝突
            counter = 1
            original_output_path = output_path
            while os.path.exists(output_path):
                name_part = os.path.splitext(original_output_path)[0]
                output_path = f"{name_part}_{counter}.pdf"
                counter += 1
            
            success, message = repair_and_unlock_pdf(file_path, output_path, None, available_packages)
            
            if success:
                success_count += 1
                success_details.append(f"{file_name} - {message}")
                print(f"  ✓ 成功: {message}")
            else:
                failed_files.append(f"{file_name} - {message}")
                print(f"  ✗ 失敗: {message}")
        
        except Exception as e:
            error_msg = f"處理時發生未預期錯誤: {str(e)}"
            failed_files.append(f"{file_name} - {error_msg}")
            print(f"  ✗ 錯誤: {error_msg}")
    
    # 顯示完成訊息
    print(f"\n處理完成！成功: {success_count}/{len(file_paths)}")
    
    result_message = f"處理完成!\n總計: {len(file_paths)} 個檔案\n成功: {success_count} 個\n失敗: {len(failed_files)} 個"
    
    if success_details:
        result_message += f"\n\n✓ 成功處理的檔案:\n" + "\n".join(success_details[:5])
        if len(success_details) > 5:
            result_message += f"\n... 還有 {len(success_details) - 5} 個檔案"
    
    if failed_files:
        result_message += f"\n\n✗ 失敗的檔案:\n" + "\n".join(failed_files[:3])
        if len(failed_files) > 3:
            result_message += f"\n... 還有 {len(failed_files) - 3} 個失敗"
    
    # 強制創建新的root視窗來顯示結果
    try:
        result_root = tk.Tk()
        result_root.withdraw()  # 隱藏主視窗
        
        if success_count > 0:
            messagebox.showinfo("處理完成", result_message)
        else:
            messagebox.showerror("處理失敗", result_message + "\n\n建議:\n1. 檢查PDF檔案是否損壞\n2. 嘗試用其他PDF閱讀器打開\n3. 安裝Ghostscript以獲得更好的修復效果")
        
        result_root.destroy()
    except Exception as e:
        print(f"顯示結果對話框時出錯: {e}")
        print("結果:")
        print(result_message)

def unlock_pdfs_with_password():
    """針對需要密碼的PDF提供密碼輸入功能"""
    print("正在檢查並安裝必要套件...")
    available_packages = check_and_install_packages()
    
    if not any(available_packages.values()):
        messagebox.showerror("錯誤", "無法安裝任何PDF處理套件")
        return
    
    # 選擇PDF檔案
    root = tk.Tk()
    root.withdraw()
    file_paths = filedialog.askopenfilenames(
        title="選擇需要密碼解鎖的PDF檔案",
        filetypes=[("PDF檔案", "*.pdf")]
    )
    
    if not file_paths:
        messagebox.showinfo("提示", "未選擇任何檔案")
        return
    
    # 創建密碼輸入對話框
    password_window = tk.Toplevel()
    password_window.title("輸入PDF密碼")
    password_window.geometry("350x180")
    password_window.resizable(False, False)
    
    tk.Label(password_window, text="請輸入PDF密碼:", font=("Arial", 12)).pack(pady=15)
    password_var = tk.StringVar()
    password_entry = tk.Entry(password_window, textvariable=password_var, show="*", width=35, font=("Arial", 11))
    password_entry.pack(pady=5)
    
    # 顯示密碼選項
    show_password_var = tk.BooleanVar()
    show_password_check = tk.Checkbutton(password_window, text="顯示密碼", 
                                        variable=show_password_var,
                                        command=lambda: password_entry.config(show="" if show_password_var.get() else "*"))
    show_password_check.pack(pady=5)
    
    result = {"password": None, "cancelled": False}
    
    def on_ok():
        result["password"] = password_var.get()
        password_window.destroy()
    
    def on_cancel():
        result["cancelled"] = True
        password_window.destroy()
    
    def on_enter(event):
        on_ok()
    
    password_entry.bind('<Return>', on_enter)
    
    button_frame = tk.Frame(password_window)
    button_frame.pack(pady=20)
    tk.Button(button_frame, text="確定", command=on_ok, width=10).pack(side=tk.LEFT, padx=10)
    tk.Button(button_frame, text="取消", command=on_cancel, width=10).pack(side=tk.LEFT, padx=10)
    
    password_entry.focus()
    password_window.wait_window()
    
    if result["cancelled"] or not result["password"]:
        return
    
    password = result["password"]
    success_count = 0
    failed_files = []
    success_details = []
    
    print(f"\n開始處理 {len(file_paths)} 個需要密碼的檔案...")
    
    for i, file_path in enumerate(file_paths, 1):
        try:
            file_dir = os.path.dirname(file_path)
            file_name = os.path.basename(file_path)
            file_name_without_ext = os.path.splitext(file_name)[0]
            
            print(f"\n[{i}/{len(file_paths)}] 正在處理: {file_name}")
            
            if "_已解鎖" in file_name_without_ext:
                base_name = file_name_without_ext.replace("_已解鎖", "")
                output_path = os.path.join(file_dir, f"{base_name}_重新修復.pdf")
            else:
                output_path = os.path.join(file_dir, f"{file_name_without_ext}_已修復.pdf")
            
            counter = 1
            original_output_path = output_path
            while os.path.exists(output_path):
                name_part = os.path.splitext(original_output_path)[0]
                output_path = f"{name_part}_{counter}.pdf"
                counter += 1
            
            success, message = repair_and_unlock_pdf(file_path, output_path, password, available_packages)
            
            if success:
                success_count += 1
                success_details.append(f"{file_name} - {message}")
                print(f"  ✓ 成功: {message}")
            else:
                failed_files.append(f"{file_name} - {message}")
                print(f"  ✗ 失敗: {message}")
            
        except Exception as e:
            error_msg = f"處理時發生錯誤: {str(e)}"
            failed_files.append(f"{file_name} - {error_msg}")
            print(f"  ✗ 錯誤: {error_msg}")
    
    # 顯示結果
    print(f"\n處理完成！成功: {success_count}/{len(file_paths)}")
    
    result_message = f"處理完成!\n總計: {len(file_paths)} 個檔案\n成功: {success_count} 個\n失敗: {len(failed_files)} 個"
    
    if success_details:
        result_message += f"\n\n✓ 成功處理的檔案:\n" + "\n".join(success_details[:5])
        if len(success_details) > 5:
            result_message += f"\n... 還有 {len(success_details) - 5} 個檔案"
    
    if failed_files:
        result_message += f"\n\n✗ 失敗的檔案:\n" + "\n".join(failed_files[:3])
        if len(failed_files) > 3:
            result_message += f"\n... 還有 {len(failed_files) - 3} 個失敗"
    
    # 強制創建新的root視窗來顯示結果
    try:
        result_root = tk.Tk()
        result_root.withdraw()  # 隱藏主視窗
        
        if success_count > 0:
            messagebox.showinfo("處理完成", result_message)
        else:
            messagebox.showerror("處理失敗", result_message)
        
        result_root.destroy()
    except Exception as e:
        print(f"顯示結果對話框時出錯: {e}")
        print("結果:")
        print(result_message)

def main():
    """主選單"""
    root = tk.Tk()
    root.title("多引擎PDF修復工具 v3.0")
    root.geometry("600x400")
    root.resizable(False, False)
    
    # 設定關閉視窗時的處理
    def on_closing():
        print("\n程式已退出，感謝使用！")
        root.quit()
        root.destroy()
        sys.exit(0)
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    # 標題
    title_label = tk.Label(root, text="多引擎PDF修復工具", font=("Arial", 20, "bold"), fg="darkblue")
    title_label.pack(pady=20)
    
    # 說明
    info_frame = tk.Frame(root)
    info_frame.pack(pady=15)
    
    info_text = """本工具使用多種PDF處理引擎來修復和解鎖PDF檔案：
    
✓ PyMuPDF - 強大的PDF處理引擎
✓ PyPDF2 - 經典的Python PDF庫  
✓ pikepdf - 基於QPDF的高效處理
✓ Ghostscript - 專業的PDF修復工具
✓ 簡單複製 - 最後的備選方案

適用於各種PDF問題：加密、損壞、格式錯誤等"""
    
    info_label = tk.Label(info_frame, text=info_text, font=("Arial", 11), justify=tk.LEFT, fg="darkgreen")
    info_label.pack()
    
    # 按鈕框架
    button_frame = tk.Frame(root)
    button_frame.pack(pady=30)
    
    def run_auto_unlock():
        """執行自動解鎖並保持主視窗"""
        try:
            unlock_pdfs()
        except Exception as e:
            messagebox.showerror("錯誤", f"執行過程中發生錯誤:\n{str(e)}")
    
    def run_password_unlock():
        """執行密碼解鎖並保持主視窗"""
        try:
            unlock_pdfs_with_password()
        except Exception as e:
            messagebox.showerror("錯誤", f"執行過程中發生錯誤:\n{str(e)}")
    
    def exit_program():
        """退出程式"""
        print("\n程式已退出，感謝使用！")
        root.quit()
        root.destroy()
        sys.exit(0)
    
    # 自動解鎖按鈕
    auto_button = tk.Button(button_frame, text="自動修復\n(無密碼或僅安全限制)", 
                           command=run_auto_unlock,
                           width=22, height=4, font=("Arial", 12, "bold"), 
                           bg="lightgreen", fg="darkgreen")
    auto_button.pack(side=tk.LEFT, padx=20)
    
    # 密碼解鎖按鈕
    password_button = tk.Button(button_frame, text="密碼修復\n(需要輸入密碼)", 
                               command=run_password_unlock,
                               width=22, height=4, font=("Arial", 12, "bold"),
                               bg="lightblue", fg="darkblue")
    password_button.pack(side=tk.LEFT, padx=20)
    
    # 退出按鈕
    quit_button = tk.Button(root, text="退出程式", command=exit_program,
                           width=15, height=2, font=("Arial", 10),
                           bg="lightcoral", fg="darkred")
    quit_button.pack(pady=10)
    
    # 底部說明
    bottom_frame = tk.Frame(root)
    bottom_frame.pack(pady=10)
    
    bottom_text = """使用建議：
1. 如果PDF損壞嚴重，建議先安裝Ghostscript獲得最佳修復效果
2. 程式會自動安裝缺少的Python套件
3. 支援批量處理，自動避免檔案名衝突
4. 處理完成後可繼續使用或點擊退出
5. 直接關閉視窗也會正常退出程式"""
    
    bottom_label = tk.Label(bottom_frame, text=bottom_text, font=("Arial", 9), 
                           justify=tk.LEFT, fg="gray")
    bottom_label.pack()
    
    try:
        root.mainloop()
    except KeyboardInterrupt:
        print("\n程式被中斷，正在退出...")
    finally:
        print("\n程式已完全關閉。")
        sys.exit(0)

if __name__ == "__main__":
    main()