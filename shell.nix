{pkgs ? import <nixpkgs> {}}:
with pkgs;
let
  my-python-packages = python-packages: with python-packages; [
    scikitlearn
    numpy
    pandas
    seaborn
    jupyter
  ];
  python-with-my-packages = python3.withPackages my-python-packages;
in
  python-with-my-packages.env
