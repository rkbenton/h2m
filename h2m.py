#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "markdownify>=1.2.2",
#     "pyobjc-framework-cocoa>=12.1",
# ]
# ///
"""
Function: 
    Takes HTML content from the macOS pasteboard, converts it to 
    GitHub-Flavored Markdown (GFM), and copies the result back to 
    the pasteboard as plain text.

How to run:
See: https://docs.astral.sh/uv/guides/scripts/#declaring-script-dependencies

We are using inline dependencies, so you can just say:
```
uv run h2m.py
```

Also, note the shebang at top. Ensure that h2m.py is executable, e.g., with chmod +x greet, then run the script:

```
./h2m
```

"""

import markdownify
from AppKit import NSPasteboard, NSPasteboardTypeHTML, NSPasteboardTypeString
import sys

def convert():
    pb = NSPasteboard.generalPasteboard()
    
    # 1. Audit available flavors
    flavors = pb.types()
    print("📋 Pasteboard Flavor Audit:")
    if not flavors:
        print("  [Empty Pasteboard]")
    else:
        for flavor in flavors:
            print(f"  - {flavor}")
    print("-" * 35)

    # 2. Attempt to grab HTML
    html_data = pb.stringForType_(NSPasteboardTypeHTML)
    
    if not html_data:
        # Fallback: Check if plain text contains HTML-like tags
        text_data = pb.stringForType_(NSPasteboardTypeString)
        if text_data and "<" in text_data and ">" in text_data:
            print("⚠️  No native HTML flavor found. Parsing plain text as HTML...")
            html_data = text_data
        else:
            print("❌ Error: No HTML content found in the pasteboard.", file=sys.stderr)
            return

    # 3. Convert with GFM settings and Attribute Cleaning
    try:
        # markdownify ignores most attributes by default, but we'll 
        # explicitly strip out problematic tags to keep it lean.
        markdown = markdownify.markdownify(
            html_data,
            heading_style="ATX",      # Use # for headers
            bullets="-",              # GFM dash bullets
            code_language="python",   # Default code block language
            strip=["script", "style", "meta", "link", "noscript"],
            # Ensure we don't carry over IDs/Classes (handled by markdownify's default behavior)
        ).strip()

        if not markdown:
            print("⚠️  Conversion resulted in empty text. Pasteboard remains unchanged.")
            return

        # 4. Write back to pasteboard
        pb.clearContents()
        pb.setString_forType_(markdown, NSPasteboardTypeString)
        
        print(f"✅ Success!")
        print(f"   Input:  {len(html_data)} characters (HTML)")
        print(f"   Output: {len(markdown)} characters (GFM Markdown)")
        print("🚀 Your pasteboard now contains the Markdown version.")

    except Exception as e:
        print(f"❌ An unexpected error occurred during conversion: {e}", file=sys.stderr)

if __name__ == "__main__":
    convert()