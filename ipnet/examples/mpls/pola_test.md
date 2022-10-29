# Pola Test

`sr_mpls_vpn_10.py`

## setup
```
go install github.com/nttcom/pola/cmd/polad@latest
go install github.com/nttcom/pola/cmd/pola@latest
```

## PCE

in pce xterm.
```
su vagrant  # for go env
sudo ~/go/bin/polad -f polad/config.yaml
```

in another pce xterm.
```
su vagrant  # for go env
sudo ~/go/bin/pola -f polad/<sr_policy_file>.yaml
```