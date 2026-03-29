{
  description = "A nix development shell";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    systems.url = "github:nix-systems/default";
    flake-utils = {
      url = "github:numtide/flake-utils";
      inputs.systems.follows = "systems";
    };
  };

  outputs = {
    nixpkgs,
    flake-utils,
    ...
  }:
    flake-utils.lib.eachDefaultSystem (
      system: let
        lib = nixpkgs.lib;
        pkgs = import nixpkgs {
          inherit system;
          config.allowUnfree = true;
        };
        buildInputs = with pkgs; [
          openssl
          pkg-config

          # https://github.com/iced-rs/iced/blob/fd5ed0d0a6e84b3c036ff8e1f0d62d383d4b1e82/DEPENDENCIES.md#nixos
          expat
          fontconfig
          freetype
          freetype.dev
          libGL
          pkg-config
          xorg.libX11
          xorg.libXcursor
          xorg.libXi
          xorg.libXrandr
          wayland
          libxkbcommon
        ];
      in {
        inherit lib;

        devShells.default = pkgs.mkShell {
          inherit buildInputs;

          LD_LIBRARY_PATH = builtins.foldl' (a: b: "${a}:${b}/lib") "${pkgs.vulkan-loader}/lib" buildInputs;

          packages = with pkgs;
            [
              go
              gopls
              gotools
              golangci-lint
              go-swag

              yarn
              python3
            ]
            ++ (with python3.pkgs; [
              requests
              fastapi
              uvicorn
            ]);
        };
      }
    );
}
