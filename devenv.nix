{ pkgs, lib, config, inputs, ... }:

{
  # https://devenv.sh/basics/
  # secrets.env.enable = true;

  # https://devenv.sh/packages/
  packages = [
    pkgs.libGL
    pkgs.libglvnd
    pkgs.glib
  ];

  # https://devenv.sh/languages/

  languages.python = {
    enable = true;

    venv.enable = true;
    venv.requirements = ./requirements.txt;
  };
  # https://devenv.sh/processes/
  # processes.cargo-watch.exec = "cargo-watch";
  processes.backend.exec = "python app.py";
  processes.frontedn.exec = "npm run dev";

  # https://devenv.sh/services/
  # services.postgres.enable = true;

  # https://devenv.sh/scripts/
  scripts.hello.exec = ''
    echo hello from $GREET
  '';

  enterShell = ''
    hello
    git --version
  '';

  # https://devenv.sh/tasks/
  # tasks = {
  #   "myproj:setup".exec = "mytool build";
  #   "devenv:enterShell".after = [ "myproj:setup" ];
  # };

  # https://devenv.sh/tests/
  enterTest = ''
    echo "Running tests"
    git --version | grep --color=auto "${pkgs.git.version}"
  '';

  # https://devenv.sh/pre-commit-hooks/
  # pre-commit.hooks.shellcheck.enable = true;

  # See full reference at https://devenv.sh/reference/options/
}
