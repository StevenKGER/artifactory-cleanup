import json

from artifactory_cleanup.rules.utils import (
    artifacts_list_to_tree,
    folder_artifacts_without_children,
)


def load_artifacts():
    """
    test-repo
        - .
        - user1
          - package1
            - 0.1.2
              - testing
                - ee9a7171a4577b0077ba521a2a16411f
                  - export
                    - conanfile.py | FILE
                    - conanmanifest.txt | FILE
                  - package
                    - 9bfdcfa2bb925892ecf42e2a018a3f3529826676
                      - bb158820ff3cdfb0764acd8abd0fcb05
                        - conan_package.tgz | FILE
                        - conaninfo.txt | FILE
                        - conanmanifest.txt | FILE
                - 6a5ffb1868d640cbcb78c934c4728895
                  - export
                    - conanfile.py | FILE
                    - conanmanifest.txt | FILE
                  - package
                    - 9bfdcfa2bb925892ecf42e2a018a3f3529826676
                      - 53518c74f2e9410bb2f6df473adee01f
                        - conan_package.tgz | FILE
                        - conaninfo.txt | FILE
                        - conanmanifest.txt | FILE
        - user2
          - package5
          - package2
            - 4.2.0
              - testing
                - 18259fd357457eed2a5b2dffede67385
                  - export
                    - conanfile.py | FIlE
                    - conanmanifest.txt | FILE
                  - package
                    - 976790fbda33f5619b11df9030fb714af0990694
                      - 8854919f6b53ccf1c347f5a34b475b6a
                        - conan_package.tgz | FILE
                        - conaninfo.txt | FILE
                        - conanmanifest.txt | FILE
            - 4.2.1
              - testing2
                - 18259fd357457eed2a5b2dffede67385
                  - package
                    - 976790fbda33f5619b11df9030fb714af0990694
                      - e708164fb64d5cce0bef0354b59a17ac
                      - ba38761e49a42a9a44c8be1e30df4886
        - user3
    """
    with open("artifacts_list.json", "r") as fp:
        artifacts_list = json.load(fp)
    return artifacts_list


def test_folder_artifacts_without_children():
    artifacts_list = load_artifacts()

    artifacts_tree = artifacts_list_to_tree(artifacts_list)
    empty_folders = folder_artifacts_without_children(artifacts_tree)

    expected_empty_folders = [
        # Simple empty folder without children in the list, at a deeper level
        {
            "repo": "test-repo",
            "path": "user2/package2",
            "name": "4.2.1",
            "type": "folder",
            "size": 0,
            "depth": 3,
        },
        # Simple empty folder without children at a higher level
        {
            "repo": "test-repo",
            "path": "user2",
            "name": "package5",
            "type": "folder",
            "size": 0,
            "depth": 2,
        },
        # Longer folder structure where all subfolders are empty
        {
            "repo": "test-repo",
            "path": "",
            "name": "user3",
        },
    ]
    assert list(empty_folders) == expected_empty_folders
