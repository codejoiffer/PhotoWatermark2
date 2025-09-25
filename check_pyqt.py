#!/usr/bin/env python3
# 检查PyQt6模块中可用的组件
print("尝试导入PyQt6...")
try:
    import PyQt6
    print(f"PyQt6版本: {PyQt6.__version__}")
except Exception as e:
    print(f"导入PyQt6失败: {e}")

print("\n尝试导入PyQt6.QtWidgets...")
try:
    from PyQt6 import QtWidgets
    print("成功导入PyQt6.QtWidgets")
except Exception as e:
    print(f"导入PyQt6.QtWidgets失败: {e}")

print("\n尝试导入PyQt6.QtGui...")
try:
    from PyQt6 import QtGui
    print("成功导入PyQt6.QtGui")
except Exception as e:
    print(f"导入PyQt6.QtGui失败: {e}")

print("\n尝试导入PyQt6.QtCore...")
try:
    from PyQt6 import QtCore
    print("成功导入PyQt6.QtCore")
except Exception as e:
    print(f"导入PyQt6.QtCore失败: {e}")

print("\n检查QtWidgets中的组件是否以Q开头...")
try:
    from PyQt6 import QtWidgets
    # 只打印以'Q'开头的前20个组件
    q_components = [attr for attr in dir(QtWidgets) if attr.startswith('Q')]
    print(f"QtWidgets中以'Q'开头的组件数量: {len(q_components)}")
    print("前20个以'Q'开头的组件:")
    for comp in q_components[:20]:
        print(f"  - {comp}")

except Exception as e:
    print(f"检查组件失败: {e}")

print("\n检查QAction的位置...")
try:
    # 尝试从不同模块导入QAction
    try:
        from PyQt6.QtWidgets import QAction
        print("✓ QAction在PyQt6.QtWidgets中可用")
    except ImportError:
        try:
            from PyQt6.QtGui import QAction
            print("✓ QAction在PyQt6.QtGui中可用")
        except ImportError:
            try:
                from PyQt6.QtCore import QAction
                print("✓ QAction在PyQt6.QtCore中可用")
            except ImportError:
                print("✗ 无法找到QAction")
except Exception as e:
    print(f"检查QAction失败: {e}")