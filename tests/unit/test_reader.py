#!/usr/bin/python
import os.path as path
from nose.tools import eq_, assert_in
from parameterized import parameterized

from ExcelRobot.reader import ExcelReader, DataType

CURRENT_DIR = path.dirname(path.abspath(__file__))
DATA_DIR = path.join(CURRENT_DIR, '../data')


# def setup_module():
#     print('Setup module')


# def teardown_module():
#     print('Teardown module')


@parameterized([
    ('ExcelRobotTest.xls', 5),
    ('ExcelRobotTest.xlsx', 5)
])
def test_open(input_file, expected):
    reader = ExcelReader(path.join(DATA_DIR, input_file))
    eq_(expected, reader.get_number_of_sheets())


@parameterized([
    ('ExcelRobotTest.xls', 'TestSheet1'),
    ('ExcelRobotTest.xlsx', 'TestSheet1')
])
def test_sheet_name(input_file, expected):
    reader = ExcelReader(path.join(DATA_DIR, input_file))
    assert_in(expected, reader.get_sheet_names())


@parameterized([
    ('ExcelRobotTest.xls', 'TestSheet1', 2, 3),
    ('ExcelRobotTest.xlsx', 'TestSheet1', 2, 3)
])
def test_sheet_size(input_file, sheet_name, col_count, row_count):
    reader = ExcelReader(path.join(DATA_DIR, input_file))
    eq_(col_count, reader.get_column_count(sheet_name))
    eq_(row_count, reader.get_row_count(sheet_name))


@parameterized([
    ('ExcelRobotTest.xls', 'TestSheet1', 0, [('A1', 'This is a test sheet'), ('A2', 'User1'), ('A3', 'User2')]),
    ('ExcelRobotTest.xls', 'TestSheet1', 1, [('B1', 'Points'), ('B2', 57), ('B3', 5178)]),
    ('ExcelRobotTest.xlsx', 'TestSheet1', 0, [('A1', 'This is a test sheet'), ('A2', 'User1'), ('A3', 'User2')]),
    ('ExcelRobotTest.xlsx', 'TestSheet1', 1, [('B1', 'Points'), ('B2', 57), ('B3', 5178)]),
])
def test_get_col_values(input_file, sheet_name, column, expected):
    reader = ExcelReader(path.join(DATA_DIR, input_file))
    eq_(expected, reader.get_column_values(sheet_name, column))


@parameterized([
    ('ExcelRobotTest.xls', 'TestSheet2', 0, [('A1', 'This is a test sheet'), ('B1', 'Date of Birth')]),
    ('ExcelRobotTest.xls', 'TestSheet2', 1, [('A2', 'User3'), ('B2', '23.8.1982')]),
    ('ExcelRobotTest.xlsx', 'TestSheet2', 0, [('A1', 'This is a test sheet'), ('B1', 'Date of Birth')]),
    ('ExcelRobotTest.xlsx', 'TestSheet2', 1, [('A2', 'User3'), ('B2', '23.8.1982')]),
])
def test_get_row_values(input_file, sheet_name, column, expected):
    reader = ExcelReader(path.join(DATA_DIR, input_file))
    eq_(expected, reader.get_row_values(sheet_name, column))


@parameterized([
    ('ExcelRobotTest.xls', 'TestSheet1', 'a2', 'User1'),
    ('ExcelRobotTest.xls', 'TestSheet1', 'B2', 57),
    ('ExcelRobotTest.xls', 'TestSheet2', 'B2', '23.8.1982'),
    ('ExcelRobotTest.xlsx', 'TestSheet1', 'A2', 'User1'),
    ('ExcelRobotTest.xlsx', 'TestSheet1', 'B2', 57),
    ('ExcelRobotTest.xlsx', 'TestSheet2', 'B2', '23.8.1982'),
])
def test_get_cell_value_by_name(input_file, sheet_name, cell_name, expected):
    reader = ExcelReader(path.join(DATA_DIR, input_file))
    eq_(expected, reader.read_cell_data_by_name(sheet_name, cell_name))


@parameterized([
    ('ExcelRobotTest.xls', 'TestSheet1', 0, 1, 'User1'),
    ('ExcelRobotTest.xls', 'TestSheet1', 1, 1, 57),
    ('ExcelRobotTest.xls', 'TestSheet2', 1, 1, '23.8.1982'),
    ('ExcelRobotTest.xls', 'TestSheet3', 2, 1, '1982-05-14'),
    ('ExcelRobotTest.xls', 'TestSheet3', 3, 1, True),
    ('ExcelRobotTest.xlsx', 'TestSheet1', 0, 1, 'User1'),
    ('ExcelRobotTest.xlsx', 'TestSheet1', 1, 1, 57),
    ('ExcelRobotTest.xlsx', 'TestSheet2', 1, 1, '23.8.1982'),
    ('ExcelRobotTest.xlsx', 'TestSheet3', 2, 1, '1982-05-14'),
    ('ExcelRobotTest.xlsx', 'TestSheet3', 3, 1, True),
])
def test_get_cell_value_by_coord(input_file, sheet_name, col, row, expected):
    reader = ExcelReader(path.join(DATA_DIR, input_file))
    eq_(expected, reader.read_cell_data_by_coordinates(sheet_name, col, row))


@parameterized([
    ('ExcelRobotTest.xls', 'TestSheet3', 0, 1, DataType.NUMBER.name, True),
    ('ExcelRobotTest.xls', 'TestSheet3', 1, 1, DataType.TEXT.name, True),
    ('ExcelRobotTest.xls', 'TestSheet3', 2, 1, DataType.DATE.name, True),
    ('ExcelRobotTest.xls', 'TestSheet3', 3, 1, DataType.BOOL.name, True),
    ('ExcelRobotTest.xls', 'TestSheet3', 5, 1, DataType.EMPTY.name, True),
    ('ExcelRobotTest.xlsx', 'TestSheet3', 0, 1, DataType.NUMBER.name, True),
    ('ExcelRobotTest.xlsx', 'TestSheet3', 1, 1, DataType.TEXT.name, True),
    ('ExcelRobotTest.xlsx', 'TestSheet3', 2, 1, DataType.DATE.name, True),
    ('ExcelRobotTest.xlsx', 'TestSheet3', 3, 1, DataType.BOOL.name, True),
    ('ExcelRobotTest.xlsx', 'TestSheet3', 5, 1, DataType.EMPTY.name, True),
])
def test_check_cell_type(input_file, sheet_name, col, row, data_type, expected):
    reader = ExcelReader(path.join(DATA_DIR, input_file))
    eq_(expected, reader.check_cell_type(sheet_name, col, row, data_type))
