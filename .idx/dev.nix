{ pkgs, ... }: {
  # Which nixpkgs channel to use.
  channel = "stable-24.11"; # or "unstable"

  # Use https://search.nixos.org/packages to find packages
  packages = [
    pkgs.gh
    pkgs.hugo
    pkgs.go
    pkgs.python3
  ];

  # Sets environment variables in the workspace
  env = {
    # SOME_ENV_VAR = "hello";
  };

  # Search for the extensions you want on https://open-vsx.org/ and use "publisher.id"
  idx.extensions = [
    "golang.go"
    "ms-python.debugpy"
    "ms-python.python"
    "charliermarsh.ruff"
  ];

  idx.workspace.onCreate = {
    # instal-go = "go install https://github.com/soda92/evu";
  };

  # Enable previews and customize configuration
  idx.previews = {
    enable = true;
    previews = {
      web = {
        command = [
          "hugo"
          "serve"
          "--port"
          "$PORT"
          "-D"
          "--baseURL=/"
          "--appendPort=false"
        ];
        manager = "web";
        # Optionally, specify a directory that contains your web app
        # cwd = "app/client";
      };
    };
  };
}
