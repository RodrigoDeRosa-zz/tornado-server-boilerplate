FROM python:3.8 AS build
WORKDIR /src
COPY requirements.txt .
# install app dependencies
RUN pip install --user -r requirements.txt

FROM python:3.8 AS release
WORKDIR /src
COPY --from=build /root/.local /root/.local
# Copy all needed files to container's root directory
COPY server.py /
ADD /src /src
COPY /keys /keys
COPY /views /views
# Run app with this command.
CMD ["python", "/server.py", "--proc", "2", "--db_host", "mongodb", "--lock_server", "--lock_server_host", "etcd"]