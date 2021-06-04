# Kommt heute Aktenzeichen?

## Setting up Kommt heute Aktenzeichen

To set up Kommt heute Aktenzeichen, you need three things:

1. The Python version manager `pyenv`.

2. Python (any version).

3. The Python dependency manager `pipenv`.

### Installing pyenv

The Python version manager `pyenv` makes sure you can always keep
the exact Python version required by Kommt heute Aktenzeichen,
regardless of your system Python.

To install `pyenv` on Windows, run:

```
python -m pip install pyenv
```

To install `pyenv` on macOS, run:

```
brew install pyenv
```

### Checking your system-wide Python installation

Make sure you have Python (any version) installed on your system.

To check, run:

```
pip --version
```

If that fails, try:

```
pip3 --version
```

Proceed after you’ve confirmed one of those to work.

### Installing pipenv

Install `pipenv` as described under https://pipenv.pypa.io/en/latest/install/#installing-pipenv.

### Finishing up the project setup

- Go to the kommtheuteaktenzeichen directory.

- Run the following command:

```
pipenv install -d
```


## Running kommtheuteaktenzeichen

To check whether Aktenzeichen runs today, run the following command line:

```
pipenv run kha check
```

Or run the web app locally:

```
pipenv run web
```

To point the browser to the page quickly, hold down <kbd>⌘</kbd> and double-click the [http://127.0.0.1:5000/](http://127.0.0.1:5000/) URL that appears on your terminal.


## Contributing to kommtheuteaktenzeichen

### Running the tests

To execute the tests, run:

```
pipenv run tests
```

To execute a single test, run e. g.:

```
pipenv run tests -vv tests/kha/test_api.py::test_next_start
```

### Running the linter

To execute the linter, run:

```
pipenv run linter
```

### Running the static type check

To execute the static type check, run:

```
pipenv run typecheck
```


## Maintenance

### Refresh dependencies

If you get errors after a Git pull, refresh your dependencies:

```
pipenv install -d
```

### Checking dependencies for vulnerabilities

To check Kommt heute Aktenzeichen’s dependencies for known vulnerabilities, run:

```
pipenv check
```

### Checking dependencies for compatible updates

To check Kommt heute Aktenzeichen’s dependencies for compatible updates, run:

```
pipenv update --dry-run
```


## Deployment

To deploy, run:

```
pipenv run deploy
```

To redeploy, run:

```
pipenv run update
```


## Advanced: Setting up AWS from scratch

Usually you don’t need to do this.

It’s just in case the project needs to be set up from scratch with a
brand new AWS account.

Steps to set up AWS from scratch:

- Set up an AWS account and billing. For this example, the account name is `Clackcluster`.

- Install the AWS CLI. To do this on macOS, run:

    ```bash
    brew reinstall awscli
    ```

- Go to the AWS console and set up multi-factor authentication.

- Set up root user API credentials and store them in your AWS credentials file.

- Check connectivity:

    ```bash
    aws iam get-user
    ```

- Set up Zappa for your AWS account:

    ```bash
    pipenv run zappa init
    ```

- Name the environment `prod`.

- Name the private S3 bucket `kha-store`.


## Advanced: 1Password integration

If you add 1Password integration, you don’t have to expose your AWS credentials in plain text in a file.

The following steps have been tested on macOS only. The 1Password GUI has some differences among platforms so it’s not guaranteed that
it works on platforms other than macOS.

### Configuring 1Password CLI on macOS

One-time steps to configure 1Password CLI on macOS:

1. Make sure the 1Password CLI is installed and configured for your 1Password vault.

2. Make sure the `jq` utility is installed. To install or update it, run:

    ```bash
    brew reinstall jq
    ```

3. Create a login item in 1Password with two fields named `Access Key ID` and `Secret Access Key`. Fill in your AWS credentials.

4. Create a script named `op-aws-credentials-client` with the following content:

    ```bash
    #!/bin/bash
    if [ "${SKIP_AWS_SECRET:-0}" -ne '0' ]; then
      printf '\0'
      exit 0
    fi
    op get item \
      --fields='Access Key ID,Secret Access Key' \
      --vault=<your_vault_id_here> \
      <your_item_id_here> \
      | jq "$(cat << EOF
        {
          Version: 1,
          AccessKeyId: ."Access Key ID",
          SecretAccessKey: ."Secret Access Key",
        }
    EOF
        )"
    ```

5. In the 1Password for Mac GUI app, open the preferences and go to the _Advanced_ tab (it’s the rightmost one). Tick the checkboxes that enable UUID and JSON copying.

6. Replace the fragments `<your_vault_id_here>` and `<your_item_id_here>` with the actual vault UUID and login item UUID. To obtain those UUIDs, consult the context menu of your login item.

7. Create a file `config` in your `~/.aws` directory if it’s not already there.

8. Edit your `~/.aws/config` as follows:

    ```
    [default]
    credential_process = /path/to/op-aws-credentials-client
    ```

9. Replace the fragment `/path/to/op-aws-credentials-client` with the actual path to your `op-aws-credentials-client` script.


## License

Copyright (c) 2021 The kommtheuteaktenzeichen authors

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
For a copy of the License, see [LICENSE](LICENSE).
