function all_mets = import_all_mets(filename, startRow, endRow)
%IMPORTFILE1 Import numeric data from a text file as column vectors.
%   C00001 = IMPORTFILE1(FILENAME) Reads data from text file FILENAME for
%   the default selection.
%
%   C00001 = IMPORTFILE1(FILENAME, STARTROW, ENDROW) Reads data from rows
%   STARTROW through ENDROW of text file FILENAME.
%
% Example:
%   C00001 = importfile1('all_mets.csv',1, 1591);
%
%    See also TEXTSCAN.

% Auto-generated by MATLAB on 2016/05/25 00:13:13

%% Initialize variables.
delimiter = '';
if nargin<=2
    startRow = 1;
    endRow = inf;
end

%% Format string for each line of text:
%   column1: text (%s)
% For more information, see the TEXTSCAN documentation.
formatSpec = '%s%[^\n\r]';

%% Open the text file.
fileID = fopen(filename,'r');

%% Read columns of data according to format string.
% This call is based on the structure of the file used to generate this
% code. If an error occurs for a different file, try regenerating the code
% from the Import Tool.
dataArray = textscan(fileID, formatSpec, endRow(1)-startRow(1)+1, 'Delimiter', delimiter, 'HeaderLines', startRow(1)-1, 'ReturnOnError', false);
for block=2:length(startRow)
    frewind(fileID);
    dataArrayBlock = textscan(fileID, formatSpec, endRow(block)-startRow(block)+1, 'Delimiter', delimiter, 'HeaderLines', startRow(block)-1, 'ReturnOnError', false);
    dataArray{1} = [dataArray{1};dataArrayBlock{1}];
end

%% Close the text file.
fclose(fileID);

%% Post processing for unimportable data.
% No unimportable data rules were applied during the import, so no post
% processing code is included. To generate code which works for
% unimportable data, select unimportable cells in a file and regenerate the
% script.

%% Allocate imported array to column variable names
all_mets = dataArray{:, 1};


