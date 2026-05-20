import os
import shutil

def copy_assets():
    base_dir = "e:/FoodSafety_Malnutrition/FoodSafety_Malnutrition"
    assets_dir = os.path.join(base_dir, "frontend", "public", "assets")
    
    os.makedirs(assets_dir, exist_ok=True)
    
    # Directories to copy from
    plots_dir = os.path.join(base_dir, "outputs", "plots")
    reports_dir = os.path.join(base_dir, "outputs", "reports")
    
    count = 0
    
    if os.path.exists(plots_dir):
        for file in os.listdir(plots_dir):
            if file.endswith('.png') or file.endswith('.html'):
                src = os.path.join(plots_dir, file)
                dst = os.path.join(assets_dir, file)
                shutil.copy2(src, dst)
                count += 1
                
    if os.path.exists(reports_dir):
        for file in os.listdir(reports_dir):
            if file.endswith('.txt'):
                src = os.path.join(reports_dir, file)
                dst = os.path.join(assets_dir, file)
                shutil.copy2(src, dst)
                count += 1
                
    print(f"Successfully copied {count} files to {assets_dir}")

if __name__ == "__main__":
    copy_assets()
