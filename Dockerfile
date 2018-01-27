FROM kennethreitz/pipenv

COPY /* /app/

RUN pipenv install iota_mnemonic

ENTRYPOINT ["pipenv", "run", "python", "-m", "iota_mnemonic"]

