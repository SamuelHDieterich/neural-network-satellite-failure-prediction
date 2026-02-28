{ pkgs, ... }:
{
  # Packages
  packages = [ pkgs.git ];

  # Languages
  ## Python
  languages.python = {
    enable = true;
    package = pkgs.python3;
    directory = "./src";
    uv = {
      enable = true;
      package = pkgs.uv;
      sync.enable = true;
    };
  };

  # Git Hooks
  git-hooks.hooks = {
    # Python
    ruff.enable = true;
    ruff-format.enable = true;
    isort.enable = true;
  };
}
