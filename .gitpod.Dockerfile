FROM gitpod/workspace-full

# Install custom tools, runtime, etc.
RUN brew install fzf
RUN pip3 install -r requirements.txt