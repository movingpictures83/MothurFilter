import PyPluMA

class MothurFilterPlugin:
   def input(self, filename):
      self.parameters = dict()
      paramfile = open(filename, 'r')
      self.removetaxa = []
      for line in paramfile:
         contents = line.split('\t')
         if (len(contents) == 2):
            self.parameters[contents[0]] = contents[1].strip()
         else:
            self.removetaxa.append(contents[0])

      sharedfile = open(PyPluMA.prefix()+"/"+self.parameters["shared"], 'r')
      taxonomyfile = open(PyPluMA.prefix()+"/"+self.parameters["taxonomy"], 'r')
      metadata = open(PyPluMA.prefix()+"/"+self.parameters["metadata"], 'r')
      self.threshold = float(self.parameters["threshold"])
      self.firstline = sharedfile.readline().strip()
      self.header = self.firstline.split('\t')

      self.sharedcontents = []
      for line in sharedfile:
        contents = line.strip().split('\t')
        self.sharedcontents.append(contents)

      self.firstline = taxonomyfile.readline()
      self.taxonomycontents = []
      for line in taxonomyfile:
        contents = line.strip().split('\t')
        self.taxonomycontents.append(contents)


      self.groups = dict()
      line1 = metadata.readline()
      for line in metadata:
          line = line.strip()
          contents = line.split(',')
          samplename = contents[0]
          samplegroup = contents[1]
          if (samplegroup not in self.groups):
             self.groups[samplegroup] = []
          self.groups[samplegroup].append(samplename)


      print(len(self.taxonomycontents))


   def run(self):
      # Filter out Halomonas
      toRemove = []
      for i in range(len(self.taxonomycontents)):
          otuname = self.taxonomycontents[i][0]
          otudesc = self.taxonomycontents[i][2]
          for taxon in self.removetaxa:
             if (taxon) in otudesc:
                toRemove.append(otuname)
                break

      # Set taxa to zero that are not in at least 50% of samples in a group
      for group in self.groups:
          idxs = []
          for i in range(len(self.sharedcontents)):
              if ('\"'+self.sharedcontents[i][1]+'\"' in self.groups[group]):
                  idxs.append(i)

          nonzero = 0
    
          print(idxs)
          for j in range(3, len(self.header)):
              zerosum = 0
              for index in idxs:
                  if (float(self.sharedcontents[index][j]) != 0):
                      zerosum += 1
              if (float(zerosum)/len(idxs) < self.threshold):
                  print("REMOVING "+str(zerosum)+" "+str(len(idxs)))
                  for index in idxs:
                      self.sharedcontents[index][j] = str(0)


      # Remove any that are all zero
      for j in range(3, len(self.header)):
         zeroflag = True
         for i in range(len(self.sharedcontents)):
            if (float(self.sharedcontents[i][j]) != 0):
                zeroflag = False
                break
         if (zeroflag and self.header[j] not in toRemove):
             toRemove.append(self.header[j])


      # Now the removal
      for taxon in toRemove:
          idx = self.header.index(taxon)
          for j in range(len(self.sharedcontents)):
              #self.sharedcontents[j] = self.sharedcontents[j][:idx]
              self.sharedcontents[j] = self.sharedcontents[j][:idx] + self.sharedcontents[j][idx+1:]
          self.header.remove(taxon)

          for k in range(len(self.taxonomycontents)):
              if (self.taxonomycontents[k][0] == taxon):
                 self.taxonomycontents.remove(self.taxonomycontents[k])
                 break


      for i in range(len(self.sharedcontents)):
          self.sharedcontents[i][2] = str(len(self.taxonomycontents))


   def output(self, filename):
      sharedoutfile = open(filename+"/"+self.parameters["sharedout"], 'w')
      taxonomyoutfile = open(filename+"/"+self.parameters["taxonomyout"], 'w')

      for i in range(len(self.header)):
              sharedoutfile.write(self.header[i])
              if (i != len(self.header)-1):
                  sharedoutfile.write("\t")
              else:
                  sharedoutfile.write("\n")


      for element in self.sharedcontents:
          for i in range(len(element)):
              sharedoutfile.write(element[i])
              if (i != len(element)-1):
                  sharedoutfile.write("\t")
              else:
                  sharedoutfile.write("\n")



      print(len(self.taxonomycontents))
      taxonomyoutfile.write(self.firstline)
      for element in self.taxonomycontents:
          for i in range(len(element)):
              taxonomyoutfile.write(element[i])
              if (i != len(element)-1):
                  taxonomyoutfile.write("\t")
              else:
                  taxonomyoutfile.write("\n")

