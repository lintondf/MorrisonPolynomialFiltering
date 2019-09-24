package utility;
/**
 * 
 */

import java.io.IOException;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;

import org.ejml.data.DMatrixRMaj;

import ucar.ma2.Array;
import ucar.nc2.Dimension;
import ucar.nc2.Group;
import ucar.nc2.NetcdfFile;
import ucar.nc2.Variable;

/**
 * @author lintondf
 *
 */

public class TestData {
	
	NetcdfFile file;
	
	public TestData() {} // bean

	public TestData( String fileName) {
		try {
			file = NetcdfFile.open(testDataPath(fileName));
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
	
	public Group createGroup( String name ) {
		Group g = new Group(this.file, file.getRootGroup(), name);
		return g;
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
	
	public List<String> getMatchingSubGroups( Group parent, String prefix ) {
		ArrayList<String> output = new ArrayList<>();
		List<Group> groups = parent.getGroups();
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

	public Group getSubGroup(Group parent, String name) {
		List<Group> groups = parent.getGroups();
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
	
	
	public DMatrixRMaj getSubGroupVariable( String parent, String subgroup, String variable) {
		return getGroupVariable( getSubGroup( getGroup(parent), subgroup), variable);
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
	
	public void putInteger( Group group, String variable, int value) {
		throw new RuntimeException("Not implemented");
	}

	public void putScalar( Group group, String variable, double value) {
		throw new RuntimeException("Not implemented");
	}

	public void putArray( Group group, String variable, DMatrixRMaj value) {
		throw new RuntimeException("Not implemented");		
	}
	
	public void close() {}
	
	public static TestData make( String fileName) {
		return new TestData(fileName);
	}
	
}
