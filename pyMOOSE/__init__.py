# Import specific functions from your modules and expose them at the package level.
from .edit_poscar import replace_atoms, write_poscar, generate_vasp_files
from .fetcher import fetch_and_write_poscar

# You can also define __all__ for explicitness about what is exported.
__all__ = [
    "replace_atoms",
    "write_poscar",
    "generate_vasp_files",
    "fetch_and_write_poscar",
]
