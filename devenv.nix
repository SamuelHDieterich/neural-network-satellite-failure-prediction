{ pkgs, config, ... }:
{
  # Packages
  packages = with pkgs; [
    git
    zlib
  ];

  # Languages
  ## Python
  languages.python = {
    enable = true;
    package = pkgs.python3;
    directory = "./src";
    uv = {
      enable = true;
      package = pkgs.uv;
      sync = {
        enable = true;
        allGroups = true;
      };
    };
  };

  # devenv shell
  enterShell = with pkgs; ''
    # Ensure zlib is available, required for NumPy
    export LD_LIBRARY_PATH="${lib.makeLibraryPath [ zlib ]}:$LD_LIBRARY_PATH"
    # Activate the Python virtual environment
    source $DEVENV_STATE/venv/bin/activate

    # Print available scripts
    echo "Available scripts:"
    ${gnused}/bin/sed -e 's| |••|g' -e 's|=| |' <<EOF | ${util-linuxMinimal}/bin/column -t | ${gnused}/bin/sed -e 's|^|  |' -e 's|••| |g'
    ${lib.generators.toKeyValue { } (lib.mapAttrs (name: value: value.description) config.scripts)}
    EOF
  '';

  # Scripts
  scripts =
    let
      data_path = state: "$DEVENV_ROOT/data/${state}/ESA_Anomaly_Dataset";
    in
    {
      download_data = {
        description = "Download the ESA Anomaly Dataset and save it in the appropriate directory.";
        packages = with pkgs; [
          wget
          unzip
        ];
        exec = ''
          $DEVENV_ROOT/src/scripts/downlod_data.bash --output_path ${data_path "raw"}
        '';
      };
      convert_to_parquet = {
        description = "Convert the downloaded ESA Anomaly Dataset to Parquet format.";
        exec = ''
          python3 $DEVENV_ROOT/src/scripts/convert_to_parquet.py \
            --input_path ${data_path "raw"} \
            --output_path ${data_path "processed"}
        '';
      };
    };

  # Git Hooks
  git-hooks.hooks = {
    # Python
    ruff.enable = true;
    ruff-format.enable = true;
  };
}
