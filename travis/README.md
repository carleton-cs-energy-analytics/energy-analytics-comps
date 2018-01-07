1. I installed [The Travis Client](https://github.com/travis-ci/travis.rb#readme), which requires Ruby.
(I'm using the tool [rbenv](https://github.com/rbenv/rbenv)).

2. I signed in, with `travis login`

3. I followed [these instructions](https://oncletom.io/2016/travis-ssh-deploy/) to:
    
    1. Generate a dedicated SSH key (it is easier to isolate and to revoke);
    2. Encrypt the private key to make it readable only by Travis CI (so as we can commit safely too!);
    3. Copy the public key onto the remote SSH host;
    4. Cleanup after unnecessary files;
    5. Stage the modified files into Git.
   
    This looks like this:
    
    ```bash
    # generate key
    ssh-keygen -t rsa -b 4096 -C 'build@travis-ci.org' -f ./deploy_rsa
 
    # Encrypt file for Travis
    travis encrypt-file deploy_rsa --add
 
    # Add key to server
    ssh-copy-id -i deploy_rsa.pub <ssh-user>@<deploy-host>
    
    # Remove non-encryped keys, add encryped key to git
    rm -f deploy_rsa deploy_rsa.pub
    git add deploy_rsa.enc .travis.yml
    ```

```bash
gem install travis
```