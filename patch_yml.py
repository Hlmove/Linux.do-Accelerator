import re

def patch_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # Replace OS matrix
    content = re.sub(
        r'      matrix:\n        include:\n(?:          - os: [^\n]+\n            artifact_name: [^\n]+\n            package_cmd: [^\n]+\n)+',
        '      matrix:\n        include:\n          - os: windows-latest\n            artifact_name: windows-x64\n            package_cmd: cargo packager -f nsis\n          - os: windows-11-arm\n            artifact_name: windows-arm64\n            package_cmd: cargo packager -f nsis\n',
        content
    )

    # Remove build-android block until the next job
    content = re.sub(r'  build-android:\n.*?  publish-', '  publish-', content, flags=re.DOTALL)

    # Remove build-android from needs
    content = re.sub(r'      - build-android\n', '', content)
    
    with open(filepath, 'w') as f:
        f.write(content)

patch_file('.github/workflows/build-release.yml')
