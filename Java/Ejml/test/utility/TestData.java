package utility;
/**
 * 
 */

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

import org.ejml.data.DMatrixRMaj;

import com.opencsv.CSVWriter;

import ucar.ma2.Array;
import ucar.ma2.ArrayDouble;
import ucar.ma2.DataType;
import ucar.ma2.InvalidRangeException;
import ucar.nc2.Dimension;
import ucar.nc2.Group;
import ucar.nc2.NetcdfFile;
import ucar.nc2.NetcdfFileWriter;
import ucar.nc2.Variable;

/**
 * @author lintondf
 *
 */

public class TestData {
	
	NetcdfFile file;
	CSVWriter writer;
	
	public TestData() {} // bean

	public TestData( String fileName) {
		writer = null;
		try {
			file = NetcdfFile.open(testDataPath(fileName));
		} catch (Exception x) {
			file = null;
		}
	}

	public TestData( String subDir, String fileName ) {
		file = null;
		try {
			String path = testDataPath(subDir + "/" + fileName);
			try {
				File f = new File(path);
				f.delete();
			} catch (Exception x) {}
			FileWriter outputfile = new FileWriter(path); 
	        writer = new CSVWriter(outputfile, ',', CSVWriter.NO_QUOTE_CHARACTER, CSVWriter.NO_ESCAPE_CHARACTER, CSVWriter.DEFAULT_LINE_END);
		} catch (Exception x) {
			file = null;
		}
	}
	
	public static String testDataPath( String fileName ) {
		Path currentRelativePath = Paths.get("");
		Path cwd = currentRelativePath.toAbsolutePath();
		cwd = cwd.getParent().resolve("testdata");
		return cwd.resolve(fileName).toString();
	}
	
	public List<String> getMatchingGroups( String prefix ) {
		ArrayList<String> output = new ArrayList<>();
		Group root = file.getRootGroup();
		List<Group> groups = root.getGroups();
		for (Group group : groups) {
			if (group.getShortName().startsWith(prefix)) 
				output.add(group.getShortName());
		}
		return output;
	}
	
	public Group getGroup(String name) {
		Group root = file.getRootGroup();
		List<Group> groups = root.getGroups();
		for (Group group : groups) {
			if (group.getShortName().equals(name))
				return group;
		}
		return null;
	}

	public DMatrixRMaj getGroupVariable( String group, String variable) {
		return getGroupVariable( getGroup(group), variable);
		
	}
	
	public static DMatrixRMaj getGroupVariable( Group g, String variable) {
		DMatrixRMaj output;
		for (Variable v : g.getVariables()) {
			if (v.getShortName().contentEquals(variable)) {
				try {
					Array a = v.read();
					int[] dims = v.getShape();
					if (dims.length == 0) {
						output = new DMatrixRMaj(1,1, a.nextDouble() );
					} else if (dims.length == 1) {
						output = new DMatrixRMaj(dims[0], 1, 0.0);
						int i = 0;
						while (a.hasNext()) {
							output.set(i++, a.nextDouble() );
						}
					} else {
						output = new DMatrixRMaj(dims[0], dims[1], 0.0);						
						int i = 0;
						while (a.hasNext()) {
							output.set(i++, a.nextDouble() );
						}
					}
					return output;
				} catch (IOException e) {
					return null;
				}
			}
		}
		return null;
	}
	
	
	public double getScalar( Group group, String variable ) {
		for (Variable v : group.getVariables()) {
			if (v.getShortName().contentEquals(variable)) {
				try {
					return v.readScalarDouble();
				} catch (IOException e) {
					return 0.0;
				}
			}
		}
		return 0.0;
	}
	
	public int getInteger( Group group, String variable ) {
		return (int) getScalar(group, variable);
	}
	
	public DMatrixRMaj getArray( Group group, String variable ) {
		return getGroupVariable( group, variable );
	}
	
	public Group createGroup( String name ) {
		String[] header = {name};
		writer.writeNext(header);
		return null;
	}
	
	public void putInteger( Group group, String variable, int value) {
		throw new RuntimeException("Not implemented");
	}

	public void putScalar( Group group, String variable, double value) {
		throw new RuntimeException("Not implemented");
	}

	public void putArray(Group group, String variable, DMatrixRMaj value) {
		String[] header = {variable, Integer.toString(value.numRows), Integer.toString(value.numCols)};
		writer.writeNext(header);
		for (int i = 0; i < value.numRows; i++) {
			ArrayList<String> cols = new ArrayList<>();
			for (int j = 0; j < value.numCols; j++) {
				cols.add( String.format("%.16g,", value.unsafe_get(i, j)));
			}
			writer.writeNext(cols.toArray(new String[0]));
		}
	}
	
	public void close() {
		try {
			if (file != null) {
				file.close();
			}
			if (writer != null) {
				writer.close();
			}
		} catch (Exception x) {
			x.printStackTrace();
		}
	}
	
	public static TestData make( String fileName) {
		return new TestData(fileName);
	}	
}
