try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract


class DocumentProcessor:

    contract_number_starts = ["contractnummer", "leningnummer", "contractnr", "ingnummer", "kenmerk", "contracmummer", "conracmummer"]
    filter_list = ["Contractnummer", "Datum:", ":", "."]

    def retrieveContractNumber(self, filename):
        ocrText = pytesseract \
            .image_to_string(Image.open(filename).convert("L")) \
            .split('\n')
        _lineWithContractNumber = self.__findLineContractNumber(ocrText)
        _contractNumber = self.__filterContractNumberFromLine(_lineWithContractNumber)
        _contractNumberWithoutDate = self.__filterDateFromLine(_contractNumber)
        return _contractNumberWithoutDate

    def __findLineContractNumber(self, stringList):
        for line in stringList:
            for start in self.contract_number_starts:
                if start in line.lower():
                    return line

        return "not found"

    def __filterContractNumberFromLine(self, line):
        for filter_word in self.filter_list:
            line = line.replace(filter_word, "")

        line = line.strip()
        return line

    def __filterDateFromLine(self, _contractNumber):
        line = _contractNumber.split()
        line = [x for x in line if len(x) > 5 and not x.isalpha()]
        line = line[0]
        return line
