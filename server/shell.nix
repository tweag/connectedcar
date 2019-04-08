{pkgs ? import <nixpkgs> {}}:
with pkgs;
let
  my-python-packages = python-packages: with python-packages; [
    flask
  ];
  python-with-my-packages = python3.withPackages my-python-packages;
in
  mkShell {
     buildInputs = [ python-with-my-packages ];
     shellHook = ''
       FLASK_APP=$(pwd)/conncar.py
       '';
     }
