import re
with open('.github/workflows/pr-ci.yml', 'r') as f:
    content = f.read()

# Update matrix
content = re.sub(
    r'        os:\n          - ubuntu-latest\n          - windows-latest\n          - macos-15\n          - macos-15-intel',
    '        os:\n          - windows-latest',
    content
)

# Remove build-android job
content = re.sub(r'\n  build-android:\n.*', '\n', content, flags=re.DOTALL)

with open('.github/workflows/pr-ci.yml', 'w') as f:
    f.write(content)

