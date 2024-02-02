{
  description = "Python Flake";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/release-23.11";
  };

  outputs = { self, nixpkgs }:
  let
    system = "x86_64-linux";
    pkgs = import nixpkgs {
      inherit system;
    };
    py = pkgs.python312Packages;
  in
  {
  packages.${system}.default = with pkgs;
    mkShell {
      venvDir = "./.venv";
      buildInputs = [
        py.python
        py.venvShellHook
        openssl.dev
      ];
      postVenvCreation = ''
        unset SOURCE_DATE_EPOCH
        pip install -r requirements.txt
      '';

      postShellHook = ''
        unset SOURCE_DATE_EPOCH
      '';
    };
  };
}
