"""
Script khởi tạo database SQLite với dữ liệu demo.
Chạy script này để tạo database SQLite và thêm dữ liệu mẫu.

Cách sử dụng:
1. Copy .env.sqlite thành .env (hoặc sửa DATABASE_URL trong .env)
2. Chạy: python init_sqlite_db.py
3. Chạy ứng dụng: python main.py
"""

import os
import sys
import io

# Fix encoding for Windows console
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Đảm bảo sử dụng SQLite
os.environ['DATABASE_URL'] = 'sqlite:///./demo.db'

from datetime import datetime
from passlib.context import CryptContext

# Import sau khi set environment variable
from app.core.database import engine, Base, SessionLocal
from app.models.models import (
    User, DonVi, DanhHieuThiDua, HinhThucKhenThuong, HoSoKhenThuong,
    UserRole, LoaiDonVi, TrangThaiHoSo, LoaiHoSo
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def init_database():
    """Khởi tạo database và tạo dữ liệu demo."""
    
    print("=" * 50)
    print("KHỞI TẠO DATABASE SQLITE CHO DEMO")
    print("=" * 50)
    
    # Xóa database cũ nếu tồn tại
    db_file = "./demo.db"
    if os.path.exists(db_file):
        print(f"\nXóa database cũ: {db_file}")
        os.remove(db_file)
    
    # Tạo tất cả bảng
    print("\nTạo các bảng trong database...")
    Base.metadata.create_all(bind=engine)
    print("✓ Đã tạo các bảng thành công")
    
    # Tạo session
    db = SessionLocal()
    
    try:
        # ===== TẠO ĐƠN VỊ =====
        print("\nTạo đơn vị...")
        don_vi_list = [
            DonVi(ma_don_vi="DV001", ten_don_vi="Ban Giám hiệu", loai_don_vi=LoaiDonVi.KHOI_CO_QUAN, thu_tu=1),
            DonVi(ma_don_vi="DV002", ten_don_vi="Khoa Triết học", loai_don_vi=LoaiDonVi.KHOA, thu_tu=2),
            DonVi(ma_don_vi="DV003", ten_don_vi="Khoa Kinh tế chính trị", loai_don_vi=LoaiDonVi.KHOA, thu_tu=3),
            DonVi(ma_don_vi="DV004", ten_don_vi="Khoa Chủ nghĩa xã hội khoa học", loai_don_vi=LoaiDonVi.KHOA, thu_tu=4),
            DonVi(ma_don_vi="DV005", ten_don_vi="Khoa Tư tưởng Hồ Chí Minh", loai_don_vi=LoaiDonVi.KHOA, thu_tu=5),
            DonVi(ma_don_vi="DV006", ten_don_vi="Khoa Công tác đảng, công tác chính trị", loai_don_vi=LoaiDonVi.KHOA, thu_tu=6),
            DonVi(ma_don_vi="DV007", ten_don_vi="Tiểu đoàn 1", loai_don_vi=LoaiDonVi.DON_VI_TRUC_THUOC, thu_tu=7),
            DonVi(ma_don_vi="DV008", ten_don_vi="Tiểu đoàn 2", loai_don_vi=LoaiDonVi.DON_VI_TRUC_THUOC, thu_tu=8),
            DonVi(ma_don_vi="DV009", ten_don_vi="Phòng Đào tạo", loai_don_vi=LoaiDonVi.KHOI_CO_QUAN, thu_tu=9),
            DonVi(ma_don_vi="DV010", ten_don_vi="Phòng Chính trị", loai_don_vi=LoaiDonVi.KHOI_CO_QUAN, thu_tu=10),
        ]
        db.add_all(don_vi_list)
        db.commit()
        print(f"✓ Đã tạo {len(don_vi_list)} đơn vị")
        
        # ===== TẠO DANH HIỆU THI ĐUA =====
        print("\nTạo danh hiệu thi đua...")
        danh_hieu_list = [
            # Cá nhân
            DanhHieuThiDua(ma_danh_hieu="CSTD", ten_danh_hieu="Chiến sĩ thi đua cơ sở", cap_khen_thuong="Cấp cơ sở", thu_tu=1),
            DanhHieuThiDua(ma_danh_hieu="LDTT", ten_danh_hieu="Lao động tiên tiến", cap_khen_thuong="Cấp cơ sở", thu_tu=2),
            DanhHieuThiDua(ma_danh_hieu="CSTDQP", ten_danh_hieu="Chiến sĩ thi đua toàn quân", cap_khen_thuong="Cấp Bộ Quốc phòng", thu_tu=3),
            DanhHieuThiDua(ma_danh_hieu="CSTDTQ", ten_danh_hieu="Chiến sĩ thi đua toàn quốc", cap_khen_thuong="Cấp Nhà nước", thu_tu=4),
            # Tập thể
            DanhHieuThiDua(ma_danh_hieu="TTXS", ten_danh_hieu="Tập thể lao động xuất sắc", cap_khen_thuong="Cấp cơ sở", thu_tu=5),
            DanhHieuThiDua(ma_danh_hieu="DVTTXS", ten_danh_hieu="Đơn vị tiên tiến xuất sắc", cap_khen_thuong="Cấp Bộ Quốc phòng", thu_tu=6),
            DanhHieuThiDua(ma_danh_hieu="CQVMTT", ten_danh_hieu="Cờ thi đua của Bộ Quốc phòng", cap_khen_thuong="Cấp Bộ Quốc phòng", thu_tu=7),
        ]
        db.add_all(danh_hieu_list)
        db.commit()
        print(f"✓ Đã tạo {len(danh_hieu_list)} danh hiệu thi đua")
        
        # ===== TẠO HÌNH THỨC KHEN THƯỞNG =====
        print("\nTạo hình thức khen thưởng...")
        hinh_thuc_list = [
            # Cá nhân
            HinhThucKhenThuong(ma_hinh_thuc="GK", ten_hinh_thuc="Giấy khen", cap_khen_thuong="Cấp cơ sở", muc_thuong=500000, thu_tu=1),
            HinhThucKhenThuong(ma_hinh_thuc="BK", ten_hinh_thuc="Bằng khen", cap_khen_thuong="Cấp Bộ Quốc phòng", muc_thuong=1500000, thu_tu=2),
            HinhThucKhenThuong(ma_hinh_thuc="HC3", ten_hinh_thuc="Huân chương Chiến công hạng Ba", cap_khen_thuong="Cấp Nhà nước", muc_thuong=3000000, thu_tu=3),
            HinhThucKhenThuong(ma_hinh_thuc="HC2", ten_hinh_thuc="Huân chương Chiến công hạng Nhì", cap_khen_thuong="Cấp Nhà nước", muc_thuong=5000000, thu_tu=4),
            HinhThucKhenThuong(ma_hinh_thuc="HC1", ten_hinh_thuc="Huân chương Chiến công hạng Nhất", cap_khen_thuong="Cấp Nhà nước", muc_thuong=10000000, thu_tu=5),
            # Tập thể
            HinhThucKhenThuong(ma_hinh_thuc="GKTT", ten_hinh_thuc="Giấy khen tập thể", cap_khen_thuong="Cấp cơ sở", muc_thuong=2000000, thu_tu=6),
            HinhThucKhenThuong(ma_hinh_thuc="BKTT", ten_hinh_thuc="Bằng khen tập thể", cap_khen_thuong="Cấp Bộ Quốc phòng", muc_thuong=5000000, thu_tu=7),
            HinhThucKhenThuong(ma_hinh_thuc="HCQK", ten_hinh_thuc="Huân chương Quân kỳ quyết thắng", cap_khen_thuong="Cấp Nhà nước", muc_thuong=20000000, thu_tu=8),
        ]
        db.add_all(hinh_thuc_list)
        db.commit()
        print(f"✓ Đã tạo {len(hinh_thuc_list)} hình thức khen thưởng")
        
        # ===== TẠO NGƯỜI DÙNG =====
        print("\nTạo người dùng...")
        users_list = [
            User(
                username="admin",
                email="admin@sqct.edu.vn",
                hashed_password=pwd_context.hash("admin123"),
                ho_ten="Quản trị viên",
                role=UserRole.ADMIN,
                don_vi_id=1,
                is_active=True
            ),
            User(
                username="lanhdao",
                email="lanhdao@sqct.edu.vn",
                hashed_password=pwd_context.hash("lanhdao123"),
                ho_ten="Đại tá Nguyễn Văn A",
                chuc_vu="Hiệu trưởng",
                role=UserRole.LANH_DAO,
                don_vi_id=1,
                is_active=True
            ),
            User(
                username="canbo",
                email="canbo@sqct.edu.vn",
                hashed_password=pwd_context.hash("canbo123"),
                ho_ten="Trung tá Trần Văn B",
                chuc_vu="Trưởng khoa Triết học",
                role=UserRole.CAN_BO,
                don_vi_id=2,
                is_active=True
            ),
            User(
                username="user1",
                email="user1@sqct.edu.vn",
                hashed_password=pwd_context.hash("user123"),
                ho_ten="Thiếu tá Lê Văn C",
                chuc_vu="Giảng viên",
                role=UserRole.USER,
                don_vi_id=2,
                is_active=True
            ),
            User(
                username="viewonly",
                email="viewonly@sqct.edu.vn",
                hashed_password=pwd_context.hash("view123"),
                ho_ten="Nhân viên xem báo cáo",
                role=UserRole.VIEW_ONLY,
                don_vi_id=1,
                is_active=True
            ),
        ]
        db.add_all(users_list)
        db.commit()
        print(f"✓ Đã tạo {len(users_list)} người dùng")
        
        # ===== TẠO HỒ SƠ KHEN THƯỞNG MẪU =====
        print("\nTạo hồ sơ khen thưởng mẫu...")
        ho_so_list = [
            HoSoKhenThuong(
                ma_ho_so="HS20250001",
                loai_ho_so=LoaiHoSo.CA_NHAN,
                ho_ten="Đại úy Phạm Văn D",
                cap_bac="Đại úy",
                chuc_vu="Giảng viên",
                don_vi_id=2,
                danh_hieu_id=1,  # Chiến sĩ thi đua cơ sở
                hinh_thuc_id=1,  # Giấy khen
                nam_khen_thuong=2025,
                thanh_tich="Hoàn thành xuất sắc nhiệm vụ giảng dạy năm học 2024-2025",
                trang_thai=TrangThaiHoSo.DA_DUYET,
                nguoi_tao_id=3
            ),
            HoSoKhenThuong(
                ma_ho_so="HS20250002",
                loai_ho_so=LoaiHoSo.CA_NHAN,
                ho_ten="Thiếu úy Nguyễn Thị E",
                cap_bac="Thiếu úy",
                chuc_vu="Học viên",
                don_vi_id=7,
                danh_hieu_id=2,  # Lao động tiên tiến
                nam_khen_thuong=2025,
                thanh_tich="Đạt thành tích xuất sắc trong học tập và rèn luyện",
                trang_thai=TrangThaiHoSo.CHO_DUYET,
                nguoi_tao_id=4
            ),
            HoSoKhenThuong(
                ma_ho_so="HS20250003",
                loai_ho_so=LoaiHoSo.TAP_THE,
                ten_tap_the="Khoa Triết học",
                don_vi_id=2,
                danh_hieu_id=5,  # Tập thể lao động xuất sắc
                hinh_thuc_id=6,  # Giấy khen tập thể
                nam_khen_thuong=2025,
                thanh_tich="Hoàn thành xuất sắc nhiệm vụ đào tạo và nghiên cứu khoa học năm 2024",
                trang_thai=TrangThaiHoSo.DA_DUYET,
                nguoi_tao_id=2
            ),
            HoSoKhenThuong(
                ma_ho_so="HS20250004",
                loai_ho_so=LoaiHoSo.CA_NHAN,
                ho_ten="Thượng úy Trần Minh F",
                cap_bac="Thượng úy",
                chuc_vu="Giảng viên",
                don_vi_id=3,
                nam_khen_thuong=2025,
                thanh_tich="Đề tài nghiên cứu khoa học cấp trường",
                trang_thai=TrangThaiHoSo.NHAP,
                nguoi_tao_id=4
            ),
        ]
        db.add_all(ho_so_list)
        db.commit()
        print(f"✓ Đã tạo {len(ho_so_list)} hồ sơ khen thưởng mẫu")
        
        print("\n" + "=" * 50)
        print("KHỞI TẠO THÀNH CÔNG!")
        print("=" * 50)
        print("\nTài khoản đăng nhập:")
        print("-" * 50)
        print(f"{'Username':<15} {'Mật khẩu':<15} {'Vai trò':<15}")
        print("-" * 50)
        print(f"{'admin':<15} {'admin123':<15} {'Quản trị viên':<15}")
        print(f"{'lanhdao':<15} {'lanhdao123':<15} {'Lãnh đạo':<15}")
        print(f"{'canbo':<15} {'canbo123':<15} {'Cán bộ':<15}")
        print(f"{'user1':<15} {'user123':<15} {'Người dùng':<15}")
        print(f"{'viewonly':<15} {'view123':<15} {'Chỉ xem':<15}")
        print("-" * 50)
        print("\nChạy ứng dụng: python main.py")
        print("Truy cập: http://localhost:8000")
        
    except Exception as e:
        print(f"\n❌ Lỗi: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
        sys.exit(1)
    finally:
        db.close()


if __name__ == "__main__":
    init_database()
