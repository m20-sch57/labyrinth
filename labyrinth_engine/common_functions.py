def from_module_name_to_path(module: str) -> str:
    return module.replace('.', '\\')
