## Perspective transform
---
Before `First Installation` and `After Installation`, you must go to path which keep this project.

**Requirements**
1. [Miniconda](https://docs.conda.io/en/latest/miniconda.html)
2. [CUDA](https://developer.nvidia.com/cuda-downloads) (Optional if Nvidia GPU available)
3. [Cudnn](https://developer.nvidia.com/cudnn) (Optional if Nvidia GPU available)
4. หากไม่ได้ใช้เน็ตที่มหาวิทยาลัย จำเป็นต้อง VPN เข้ามาในมหาวิทยาลัยขอนแก่นก่อนถึงสามารถใช้งาน Source Code นี้ได้นะครับ

**First Installation**:
กรณีไม่มีการ์ดจอ Nvidia และ [CUDA](https://developer.nvidia.com/cuda-downloads) & [Cudnn](https://developer.nvidia.com/cudnn)
1. `conda env create -f environment.yml`
2. `conda activate PeopleCount`
3. `pip install -r requirements.txt`

กรณีมีการ์ดจอ Nvidia และ [CUDA](https://developer.nvidia.com/cuda-downloads) & [Cudnn](https://developer.nvidia.com/cudnn)
1. `conda env create -f environment_gpu.yml`
2. `conda activate PeopleCount`
3. `pip install -r .\requirements_gpu.txt --no-cache-dir`

**Run file**
1. `conda activate PeopleCount`  <== Doing this only for the first time you open a terminal.
2. `python run_grand_opening_college_of_computing_new.py`

**Description important files**:
- [run_grand_opening_college_of_computing.py](run_grand_opening_college_of_computing.py)  # main objectdections app
- [run_grand_opening_college_of_computing_new.py](run_grand_opening_college_of_computing_new.py)  # main objectdections app for science week day
- [FastAPI](sql_app/main.py)  # API controls not finished yet