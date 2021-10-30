ARCHIVE_NAME=rsyncer.tar.gz

clean:
	rm -f ${ARCHIVE_NAME}

build: clean
	tar --exclude='./__pycache__' -czf ${ARCHIVE_NAME} setup.py rsyncer
