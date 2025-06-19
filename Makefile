# Development targets
.PHONY: install test lint format type-check clean pdf pdf-xelatex pdf-pdflatex pdf-html pdf-simple install-pdf-deps verify

install:
	pip install -r requirements-dev.txt

test:
	pytest tests/ -v --cov=. --cov-report=html --cov-report=term

lint:
	flake8 .
	pylint --rcfile=.pylintrc **/*.py

format:
	black .
	isort .

type-check:
	mypy .

clean:
	rm -rf __pycache__/
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	rm -f python_tutorial.pdf python_tutorial.html
	find . -name "*.pyc" -delete
	find . -name "*.pyo" -delete

install-pdf-deps:
	@echo "📦 Installing PDF generation dependencies..."
	@echo "Choose your preferred method:"
	@echo ""
	@echo "🍎 macOS (using Homebrew):"
	@echo "  brew install --cask mactex          # For XeLaTeX/PDFLaTeX"
	@echo "  brew install wkhtmltopdf            # For HTML-based PDF"
	@echo "  brew install pandoc                 # Document converter"
	@echo ""
	@echo "🐧 Ubuntu/Debian:"
	@echo "  sudo apt update"
	@echo "  sudo apt install texlive-xetex texlive-latex-extra  # For XeLaTeX"
	@echo "  sudo apt install wkhtmltopdf        # For HTML-based PDF"
	@echo "  sudo apt install pandoc             # Document converter"
	@echo ""
	@echo "🪟 Windows:"
	@echo "  choco install miktex                # For LaTeX engines"
	@echo "  choco install wkhtmltopdf           # For HTML-based PDF"
	@echo "  choco install pandoc                # Document converter"
	@echo ""
	@echo "After installation, run 'make pdf' to generate the tutorial PDF."

pdf:
	@echo "🔍 Checking for PDF engines..."
	@which pandoc > /dev/null 2>&1 || (echo "❌ pandoc not found. Please install pandoc first." && exit 1)
	@which xelatex > /dev/null 2>&1 && $(MAKE) pdf-xelatex || \
	 which pdflatex > /dev/null 2>&1 && $(MAKE) pdf-pdflatex || \
	 which wkhtmltopdf > /dev/null 2>&1 && $(MAKE) pdf-html || \
	 $(MAKE) pdf-simple

pdf-xelatex:
	@echo "📄 Generating PDF with XeLaTeX..."
	pandoc README.md \
	  --pdf-engine=xelatex \
	  --highlight-style=tango \
	  --listings \
	  --number-sections \
	  -V documentclass=article \
	  -V papersize=a4 \
	  -V fontsize=11pt \
	  -V geometry:margin=1in \
	  -V linkcolor:blue \
	  -V mainfont="DejaVu Serif" \
	  -V monofont="DejaVu Sans Mono" \
	  -V title="Python Tutorial for Java and Go Developers" \
	  -o python_tutorial.pdf

pdf-pdflatex:
	@echo "📄 Generating PDF with PDFLaTeX..."
	pandoc README.md \
	  --pdf-engine=pdflatex \
	  --highlight-style=tango \
	  --listings \
	  --number-sections \
	  -V documentclass=article \
	  -V papersize=a4 \
	  -V fontsize=11pt \
	  -V geometry:margin=1in \
	  -V linkcolor:blue \
	  -V title="Python Tutorial for Java and Go Developers" \
	  -o python_tutorial.pdf

pdf-html:
	@echo "📄 Generating PDF via HTML..."
	pandoc README.md \
	  --to=html5 \
	  --css=<(echo "body{font-family:Arial,sans-serif;max-width:800px;margin:0 auto;padding:20px;}") \
	  --standalone \
	  --highlight-style=tango \
	  --title="Python Tutorial for Java and Go Developers" \
	  -o python_tutorial.html
	wkhtmltopdf python_tutorial.html python_tutorial.pdf
	rm python_tutorial.html

pdf-simple:
	@echo "📄 Generating PDF with pandoc's basic engine..."
	@echo "Note: For better formatting, consider installing a LaTeX engine with 'make install-pdf-deps'"
	pandoc README.md \
	  --highlight-style=tango \
	  --variable=geometry:margin=1in \
	  --variable=fontsize:11pt \
	  --variable=documentclass:article \
	  --variable=linkcolor:blue \
	  --metadata title="Python Tutorial for Java and Go Developers" \
	  --pdf-engine=weasyprint \
	  -o python_tutorial.pdf 2>/dev/null || \
	pandoc README.md \
	  --highlight-style=tango \
	  --metadata title="Python Tutorial for Java and Go Developers" \
	  -t html5 -o python_tutorial.html && \
	  echo "📄 Generated HTML version (python_tutorial.html) - you can print to PDF from your browser"

# Verify project structure
verify:
	@echo "🔍 Verifying project structure..."
	@ls -la 01_getting_started/examples/
	@ls -la 02_basic_syntax/examples/
	@ls -la 03_control_flow/examples/
	@ls -la 04_functions/examples/
	@ls -la 05_oop/examples/
	@ls -la 06_modules_and_packages/examples/
	@ls -la 07_concurrency/examples/
	@ls -la 08_python_features/examples/
	@ls -la tests/
	@echo "✅ Project structure verified!" 