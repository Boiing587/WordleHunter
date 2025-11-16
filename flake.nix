{
  description = "Python development environment";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = {
    self,
    nixpkgs,
    flake-utils,
  }:
    flake-utils.lib.eachDefaultSystem (
      system: let
        pkgs = nixpkgs.legacyPackages.${system};
        python = pkgs.python311;
      in {
        devShells.default = pkgs.mkShell {
          name = "python-dev-env";

          buildInputs = with pkgs;
            [
              yarn
            ]
            ++ [
              python
            ]
            ++ (with python.pkgs; [
              requests
              fastapi
              uvicorn
            ]);
        };
      }
    );
}
