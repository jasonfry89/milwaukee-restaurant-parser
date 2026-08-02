# Milwaukee Restaurant Grade Parser

Gets Milwaukee restaurant grades

### Installation

`python3 -m venv .venv`

`source .venv/bin/activate`

`pip3 install .`

### Run

`python mke_restaraunt_parser.py`

```
[MilwaukeeFacilitySearch(facility_id='4202335458016E20862581AA0054068E', name="WY'EAST PIZZA", address='5601 W VLIET ST', sub_type='Retail Food - Serving Meals')]
MilwaukeeFacilityInformation(facility_id='4202335458016E20862581AA0054068E', name="WY'EAST PIZZA", address='5601 W VLIET ST, MILWAUKEE, WI 53208-2123', score=99, last_inspection_date=datetime.date(2025, 10, 15), status='Permitted')
```

### Publishing

Get API key from [PyPI](https://pypi.org/)

`source .venv/bin/activate`

`python3 -m pip install --upgrade build twine`

`python3 -m build`

`python3 -m twine upload dist/*`, using your API key

