# klogs

Wrapper for "kubectl logs" with the one benefit that you never
have to try `--previous` manually, as klogs does this for you.

As a result, klogs returns all log entries that are available.

## Usage

Set an alias:

```nohighlight
alias klogs="python kubelogctl.py"
```

Then:

```nohighlight
klogs -n giantswarm -l app=aws-operator -s
```

## Future ideas

- Support execution in a docker container
- Output formatting. E. g. colorize timestamps, format and indent JSON log entries
- Filter by time, similar to `--since` or `--since-time` of kubectl.
- Make the kubectl version to use selectable (or even auto-detect based on server version)
