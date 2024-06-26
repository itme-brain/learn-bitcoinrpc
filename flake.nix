{
  description = "A very basic flake";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-24.05";
  };

  outputs = { self, nixpkgs }:
  let
    system = "x86_64-linux";
    pkgs = import nixpkgs {
      inherit system;
    };
    py = pkgs.python311Packages;

  in
  with pkgs;
  {
    devShells.${system}.default = mkShell {
      name = "Pythonic Shell";

      buildInputs = [
        python3
        gcc
        py.venvShellHook

        gmp.dev
        openssl.dev
        libffi.dev
      ];

      packages = [
        py.pip
      ];

      venvDir = "./.venv";
      postVenvCreation = ''
        pip install --upgrade wheel setuptools
        pip install -r requirements.txt
      '';

      postShellHook = ''
        export LD_LIBRARY_PATH=${lib.makeLibraryPath [
          stdenv.cc.cc
        ]}
      '';
    };
  };
}
