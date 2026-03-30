.PHONY: build publish clean

VERSION := $(shell uv run python -c "from ark_cli import __version__; print(__version__)")
WHEEL := dist/ark_cli-$(VERSION)-py3-none-any.whl
BUCKET := xmp

build:
	uv build

publish: build
	@if [ ! -f "$(WHEEL)" ]; then \
		echo "Error: $(WHEEL) not found"; \
		exit 1; \
	fi
	uv run ark-cli -p tos -a upload -bucket $(BUCKET) -i $(WHEEL) -o ark-cli/ark_cli-$(VERSION)-py3-none-any.whl

clean:
	rm -rf dist/
